#!/usr/bin/env python3
import argparse
import asyncio
import hashlib
import hmac
import json
import urllib.request
from pathlib import Path
import sys

import websockets

sys.path.append(str(Path(__file__).resolve().parent))
import rainbet  # noqa: E402


class Bot:
    def __init__(self, sid: str, secret: str):
        self.sid = sid
        self.secret = secret
        self.streak = 0
        self.target = 25
        self.game = None
        self.revealed = []
        self.crossed = 0

    def load_game(self, pack: dict) -> None:
        self.sid = pack.get("session_id", self.sid)
        self.streak = pack["streak"]
        self.target = pack.get("target", self.target)
        self.game = pack["game"]
        self.revealed = list(self.game.get("revealed", []))
        self.crossed = int(self.game.get("crossed", 0))

    def canon_view(self) -> str:
        if self.game["type"] == "mines":
            rev = ",".join(str(x) for x in sorted(self.revealed))
            return f"mines:{self.streak}:{self.game['grid_size']}:{self.game['num_mines']}:{rev}"
        return f"chicken:{self.streak}:{self.game['steps']}:{self.crossed}"

    def sign(self, view: str) -> str:
        return hmac.new(bytes.fromhex(self.secret), view.encode(), hashlib.sha256).hexdigest()

    async def send(self, ws, action: str, **extra) -> dict:
        view = self.canon_view()
        pkt = {"action": action, "view": view, "sig": self.sign(view)}
        pkt.update(extra)
        await ws.send(json.dumps(pkt))
        return json.loads(await ws.recv())


async def run(base_url: str) -> None:
    req = urllib.request.Request(base_url.rstrip("/") + "/api/sessioninfo")
    with urllib.request.urlopen(req) as r:
        info = json.loads(r.read().decode())
        cookie = r.headers.get("Set-Cookie").split(";", 1)[0]

    ws_url = "wss://" + base_url.split("://", 1)[1].rstrip("/") + "/ws"
    bot = Bot(info["session_id"], info["secret"])

    async with websockets.connect(ws_url, extra_headers=[("Cookie", cookie)]) as ws:
        hello = json.loads(await ws.recv())
        if hello.get("kind") != "hello":
            raise RuntimeError(f"unexpected hello: {hello}")
        bot.load_game(hello)

        while True:
            real = rainbet.generate_game(bot.sid, bot.streak)
            if real["type"] != bot.game["type"]:
                raise RuntimeError("server/game type mismatch")

            if real["type"] == "mines":
                total = real["grid_size"] * real["grid_size"]
                mine_set = set(real["mines"])

                while True:
                    safe = [i for i in range(total) if i not in mine_set and i not in bot.revealed]
                    if not safe:
                        break
                    m = await bot.send(ws, "reveal", tile=safe[0])
                    if m.get("kind") == "state":
                        bot.streak = m.get("streak", bot.streak)
                        bot.revealed = m["revealed"]
                        continue
                    if m.get("kind") != "result":
                        raise RuntimeError(f"unexpected message: {m}")
                    if "secret" in m:
                        bot.secret = m["secret"]
                    if "session_id" in m:
                        bot.sid = m["session_id"]
                    if "flag" in m:
                        print(m["flag"])
                        return
                    bot.load_game(m["next_game"])
                    break

            else:
                max_steps = rainbet.max_safe_steps(real["cars"])
                while bot.crossed < max_steps:
                    m = await bot.send(ws, "cross")
                    if m.get("kind") != "state":
                        raise RuntimeError(f"unexpected message: {m}")
                    bot.streak = m.get("streak", bot.streak)
                    bot.crossed = m["crossed"]

                m = await bot.send(ws, "cashout")
                if m.get("kind") != "result":
                    raise RuntimeError(f"unexpected message: {m}")
                if "secret" in m:
                    bot.secret = m["secret"]
                if "session_id" in m:
                    bot.sid = m["session_id"]
                if "flag" in m:
                    print(m["flag"])
                    return
                bot.load_game(m["next_game"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="https://rainbet.challs.umdctf.io")
    args = ap.parse_args()
    asyncio.run(run(args.url))


if __name__ == "__main__":
    main()
