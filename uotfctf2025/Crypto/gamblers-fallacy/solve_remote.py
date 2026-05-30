#!/usr/bin/env python3
"""Solve script for uoftctf2025 Crypto: gamblers-fallacy.

Strategy:
1) Collect 624 revealed `Server-Seed` values (they are raw MT19937 outputs from random.getrandbits(32)).
2) Untemper them to recover the Mersenne Twister state and clone the RNG.
3) Predict future server seeds, compute the next roll exactly, and bet all-in when roll <= 2.
4) Buy the flag once balance >= 10000.

This targets the provided remote service I/O. Use only for the CTF challenge.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import re
import socket
import sys
import time
from dataclasses import dataclass
from typing import Optional


# -------------------------
# MT19937 clone utilities
# -------------------------

def _u32(x: int) -> int:
    return x & 0xFFFFFFFF


def _unshift_right_xor(y: int, shift: int) -> int:
    # Solve: y = x ^ (x >> shift)
    x = y
    # A few iterations suffices because each pass corrects higher bits.
    for _ in range(32 // shift + 2):
        x = y ^ (x >> shift)
    return _u32(x)


def _unshift_left_xor_mask(y: int, shift: int, mask: int) -> int:
    # Solve: y = x ^ ((x << shift) & mask)
    x = y
    for _ in range(32 // shift + 2):
        x = y ^ ((x << shift) & mask)
    return _u32(x)


def untemper(y: int) -> int:
    # Reverse MT19937 tempering.
    y = _unshift_right_xor(y, 18)
    y = _unshift_left_xor_mask(y, 15, 0xEFC60000)
    y = _unshift_left_xor_mask(y, 7, 0x9D2C5680)
    y = _unshift_right_xor(y, 11)
    return _u32(y)


class MT19937:
    N = 624
    M = 397
    MATRIX_A = 0x9908B0DF
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF

    def __init__(self, state_words_624: list[int]):
        if len(state_words_624) != self.N:
            raise ValueError("Need exactly 624 state words")
        self.mt = [_u32(w) for w in state_words_624]
        # When you've observed 624 consecutive outputs, the usual clone sets index=624.
        self.index = self.N

    def twist(self) -> None:
        for i in range(self.N):
            x = (self.mt[i] & self.UPPER_MASK) + (self.mt[(i + 1) % self.N] & self.LOWER_MASK)
            xA = x >> 1
            if x & 1:
                xA ^= self.MATRIX_A
            self.mt[i] = _u32(self.mt[(i + self.M) % self.N] ^ xA)
        self.index = 0

    def extract_u32(self) -> int:
        if self.index >= self.N:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        # temper
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)
        return _u32(y)


# -------------------------
# Challenge roll computation
# -------------------------

def compute_roll(server_seed: int, client_seed: str, nonce: int) -> int:
    # Mirror chall.py exactly.
    nonce_client_msg = f"{client_seed}-{nonce}".encode()
    sig = hmac.new(str(server_seed).encode(), nonce_client_msg, hashlib.sha256).hexdigest()
    index = 0
    lucky = int(sig[index * 5 : index * 5 + 5], 16)
    while lucky >= 1e6:
        index += 1
        lucky = int(sig[index * 5 : index * 5 + 5], 16)
        if index * 5 + 5 > 129:
            lucky = 9999
            break
    return round((lucky % 1e4) * 1e-2)


# -------------------------
# Remote interaction
# -------------------------

@dataclass
class Remote:
    sock: socket.socket
    buf: bytearray

    @classmethod
    def connect(cls, host: str, port: int, timeout: float = 30.0) -> "Remote":
        s = socket.create_connection((host, port), timeout=timeout)
        s.settimeout(timeout)
        return cls(sock=s, buf=bytearray())

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass

    def _recv_more(self) -> None:
        chunk = self.sock.recv(4096)
        if not chunk:
            raise EOFError("connection closed")
        self.buf.extend(chunk)

    def recv_until(self, token: bytes, timeout: float = 30.0) -> bytes:
        deadline = time.time() + timeout
        while True:
            idx = self.buf.find(token)
            if idx != -1:
                out = bytes(self.buf[: idx + len(token)])
                del self.buf[: idx + len(token)]
                return out
            if time.time() > deadline:
                raise TimeoutError(f"timeout waiting for {token!r} (buffer has {len(self.buf)} bytes)")
            self._recv_more()

    def recv_line(self, timeout: float = 30.0) -> bytes:
        deadline = time.time() + timeout
        while True:
            nl = self.buf.find(b"\n")
            if nl != -1:
                out = bytes(self.buf[: nl + 1])
                del self.buf[: nl + 1]
                return out
            if time.time() > deadline:
                raise TimeoutError("timeout waiting for line")
            self._recv_more()

    def send_line(self, s: str) -> None:
        data = (s + "\n").encode()
        self.sock.sendall(data)


_RE_SERVER_SEED = re.compile(rb"Server-Seed:\s*(\d+)")
_RE_FINAL_BAL = re.compile(rb"Final Balance:\s*([0-9]+(?:\.[0-9]+)?)")


def _parse_final_balance(chunk: bytes) -> Optional[float]:
    m = _RE_FINAL_BAL.search(chunk)
    if not m:
        return None
    return float(m.group(1).decode())


def gamble_block_collect_seeds(r: Remote, wager: float, games: int, greed: float) -> tuple[list[int], float]:
    """Enter gamble mode and play `games` in one call, collecting Server-Seed values."""

    r.recv_until(b"> ")
    r.send_line("b")

    r.recv_until(b"Wager per game")
    r.send_line(str(wager))

    r.recv_until(b"Number of games")
    r.send_line(str(games))

    r.recv_until(b"Enter your number")
    r.send_line(str(greed))

    r.recv_until(b"Do you wish to proceed?")
    r.send_line("Y")

    seeds: list[int] = []
    final_balance: Optional[float] = None

    # Read output lines until we see the final balance line.
    while True:
        line = r.recv_line(timeout=30.0)
        m = _RE_SERVER_SEED.search(line)
        if m:
            seeds.append(int(m.group(1)))
        m2 = _RE_FINAL_BAL.search(line)
        if m2:
            final_balance = float(m2.group(1).decode())
            break

    if len(seeds) < games:
        # Drain remaining buffered output if any (defensive) and surface what happened.
        raise RuntimeError(f"expected {games} seeds, got {len(seeds)}")

    # After gamble_game finishes, it prints the main banner again; leave it in buffer for caller.
    return seeds[:games], float(final_balance)


def gamble_one(r: Remote, wager: float, greed: float) -> tuple[int, int, float]:
    """Play exactly one game. Returns (roll, server_seed, final_balance)."""

    r.recv_until(b"> ")
    r.send_line("b")

    r.recv_until(b"Wager per game")
    r.send_line(str(wager))

    r.recv_until(b"Number of games")
    r.send_line("1")

    r.recv_until(b"Enter your number")
    r.send_line(str(greed))

    r.recv_until(b"Do you wish to proceed?")
    r.send_line("Y")

    roll = None
    server_seed = None
    final_balance = None

    # One game line
    while True:
        line = r.recv_line(timeout=30.0)
        if b"Game" in line and b"Server-Seed" in line:
            # Roll: {roll:02}, ... Server-Seed: {seed}
            # Keep parsing minimal/robust.
            m = _RE_SERVER_SEED.search(line)
            if m:
                server_seed = int(m.group(1))
            m_roll = re.search(rb"Roll:\s*(\d+)", line)
            if m_roll:
                roll = int(m_roll.group(1))
            break

    # Final balance line
    while True:
        line = r.recv_line(timeout=30.0)
        m = _RE_FINAL_BAL.search(line)
        if m:
            final_balance = float(m.group(1).decode())
            break

    assert roll is not None and server_seed is not None and final_balance is not None
    return roll, server_seed, final_balance


def buy_flag(r: Remote) -> str:
    r.recv_until(b"> ")
    r.send_line("a")
    r.recv_until(b"> ")
    r.send_line("a")

    # The flag should appear as its own line; grab a couple lines.
    out = b""
    for _ in range(6):
        try:
            out += r.recv_line(timeout=3.0)
        except TimeoutError:
            break
    return out.decode(errors="replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="34.162.20.138")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--timeout", type=float, default=30.0, help="socket/read timeout in seconds")
    ap.add_argument("--client-seed", default="1337awesome")
    ap.add_argument("--collect", type=int, default=624, help="number of outputs to collect for MT cloning (624 for MT19937)")
    ap.add_argument("--wager", type=float, default=1.0, help="wager used for the initial collection block")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    r = Remote.connect(args.host, args.port, timeout=args.timeout)
    try:
        if not args.quiet:
            print(f"[+] Connected to {args.host}:{args.port}")
            print(f"[+] Collecting {args.collect} Server-Seed outputs...")

        # Collect 624 outputs with a single gamble call so min-wager check doesn't drift.
        # Greed=98 keeps loss probability low.
        seeds, balance = gamble_block_collect_seeds(r, wager=args.wager, games=args.collect, greed=98)

        if not args.quiet:
            print(f"[+] Collected {len(seeds)} outputs. Balance now ~ {balance}")

        state = [untemper(x) for x in seeds]
        mt = MT19937(state)

        # Next nonce after the collection block.
        nonce = args.collect
        client_seed = args.client_seed

        # Walk forward, using predictions to choose bets.
        # We aim for a guaranteed huge jump when predicted roll <= 2.
        steps = 0
        while balance < 10000 and steps < 5000:
            predicted_server_seed = mt.extract_u32()
            predicted_roll = compute_roll(predicted_server_seed, client_seed, nonce)

            # Decide wager/greed.
            if predicted_roll <= 2:
                wager = balance
                greed = 2
            else:
                # Advance nonce cheaply; win small when possible, eat tiny loss on 99/100.
                wager = max(balance / 800.0, 0.0001)
                greed = 98

            real_roll, real_seed, balance2 = gamble_one(r, wager=wager, greed=greed)

            if real_seed != predicted_server_seed:
                raise RuntimeError(
                    f"desync: predicted seed {predicted_server_seed} but server used {real_seed} at nonce {nonce}"
                )

            if predicted_roll != real_roll:
                raise RuntimeError(
                    f"desync: predicted roll {predicted_roll} but got {real_roll} at nonce {nonce}"
                )

            balance = balance2
            nonce += 1
            steps += 1

            if not args.quiet and (predicted_roll <= 2 or steps % 50 == 0):
                print(f"[+] step={steps} nonce={nonce-1} roll={real_roll} wager={wager} greed={greed} balance={balance}")

        if balance < 10000:
            raise RuntimeError(f"Failed to reach 10000 (balance={balance}, steps={steps})")

        if not args.quiet:
            print("[+] Balance sufficient. Buying flag...")

        flag_out = buy_flag(r)
        print(flag_out, end="")
        return 0

    finally:
        r.close()


if __name__ == "__main__":
    raise SystemExit(main())
