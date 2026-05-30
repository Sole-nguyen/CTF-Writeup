#!/usr/bin/env python3

import hashlib
import hmac
import json
import os
import secrets
import socketserver
import sys


p = int(
    "db31bb574ef7a910671b6ef12198b6529371134114ac5a6a8c74388059e1d6d"
    "74d752e95b6c14d882342d8121349135d332af88b483ae8d8112141358d57dc"
    "e46980840ba94775378c9cce6bbd3fa76d9d92ffe61ca5f10c6848019cfef9"
    "c6b7a912e4dd55fcc279146a067f28510d2bbb568b1e2d516df29192ee54b02"
    "acd8b",
    16,
)
q = int("c1dfb94320225df97076076a445ec1cdd60a731b61ef2ad94e75c42e8525fabd", 16)
g = int(
    "6b44ae1b87a580892c5c08433591cf69fc07217772e61986c79442529918201"
    "28bb9c42f8cbeb6fd71f1054b0bd190a1444e990352897f9227516ae09afd60"
    "a5f397efd3ccd748d6b99c0242a16860819952409fc449dd1ad94839cdfd50"
    "6f72d314c0c02bb480d3d609ad64ecf0bf85cb7c3c68402156d15cede9368"
    "cb65896",
    16,
)

local_secret = "c332589eebca96f3783336d6641452238aa0c72bbae17bd198ec899e2558aabc"
flag = os.getenv("FLAG", "FLAG{test_flag}")
secret = int(os.getenv("LOCK_SECRET_HEX", local_secret), 16) % q
public_key = pow(g, secret, p)
key_size = (q.bit_length() + 7) // 8


def hval(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % q


def inv(n: int) -> int:
    return pow(n % q, -1, q)


def badge_code(ticket: str) -> int:
    value = hval(("badge-seed:" + ticket).encode())
    return value or 1


def sign(msg: bytes, ticket: str) -> tuple[int, int]:
    code = badge_code(ticket)
    r = pow(g, code, p) % q
    s = (inv(code) * (hval(msg) + secret * r)) % q
    return r, s


def check_admin(nonce: bytes, seal: str) -> bool:
    key = secret.to_bytes(key_size, "big")
    good = hmac.new(key, b"unlock:" + nonce, hashlib.sha256).hexdigest()
    return hmac.compare_digest(good, seal)


banner = """SmartLock Serial Console

Commands:
  pub      show the lock certificate
  badge    issue a contractor badge
  unlock   open the admin latch
  quit     close the session
"""


class Handler(socketserver.StreamRequestHandler):
    timeout = 120

    def line(self, text: str = "") -> None:
        self.wfile.write(text.encode() + b"\n")
        self.wfile.flush()

    def ask(self, text: str) -> str:
        self.wfile.write(text.encode())
        self.wfile.flush()
        data = self.rfile.readline(512)
        return data.decode(errors="ignore").strip()

    def handle(self) -> None:
        self.line(banner)

        while True:
            cmd = self.ask("> ").lower()
            if not cmd:
                return

            if cmd == "pub":
                self.line(json.dumps({"ok": True, "model": "SL-41 field unit", "scheme": "badge-v1", "p": hex(p), "q": hex(q), "g": hex(g), "y": hex(public_key)}, separators=(",", ":")))

            elif cmd == "badge":
                name = self.ask("name: ")[:80] or "visitor"
                ticket = secrets.token_hex(6)
                msg = f"badge:{name}:{ticket}".encode()
                r, s = sign(msg, ticket)
                self.line(json.dumps({"ok": True, "name": name, "ticket": ticket, "msg": msg.decode(), "r": hex(r), "s": hex(s), "access": "contractor"}, separators=(",", ":")))

            elif cmd == "unlock":
                nonce = secrets.token_bytes(16)
                self.line("nonce: " + nonce.hex())
                seal = self.ask("seal: ")
                if check_admin(nonce, seal):
                    self.line(json.dumps({"ok": True, "door": "open", "flag": flag}))
                else:
                    self.line(json.dumps({"ok": False, "door": "closed"}))

            elif cmd in {"help", "?"}:
                self.line("Commands: pub, badge, unlock, quit")

            elif cmd in {"quit", "exit"}:
                self.line("bye")
                return

            else:
                self.line("unknown command")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else os.getenv("HOST", "0.0.0.0")
    port = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv("PORT", "1337"))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((host, port), Handler) as srv:
        print(f"listening on {host}:{port}", flush=True)
        srv.serve_forever()


if __name__ == "__main__":
    main()
