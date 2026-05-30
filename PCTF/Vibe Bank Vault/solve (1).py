#!/usr/bin/env python3
import base64
import math
import os
import re
import socket
import string
import threading

import bcrypt

HOST = "18.212.136.134"
PORT = 6666
_STATIC_SALT = b"$2b$12$C8YQMlqDyz3vGN9VOGBeGu"
ALPHABET = string.ascii_letters + string.digits
PREFIX = "XCORP_VAULT_ADMIN"


def vibe_hash(data: str) -> str:
    payload = data.encode()
    portion = payload[: len(payload) % 256]
    digest = bcrypt.hashpw(portion, _STATIC_SALT)
    return "vb$1$" + base64.b64encode(digest).decode()


class Conn:
    def __init__(self, host: str, port: int):
        self.sock = socket.create_connection((host, port))
        self.buffer = b""

    def close(self):
        self.sock.close()

    def read_until(self, marker: bytes) -> str:
        while marker not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            self.buffer += chunk
        idx = self.buffer.find(marker)
        if idx == -1:
            data = self.buffer
            self.buffer = b""
        else:
            idx_end = idx + len(marker)
            data = self.buffer[:idx_end]
            self.buffer = self.buffer[idx_end:]
        text = data.decode("utf-8", errors="replace")
        print(text, end="")
        return text

    def read_all(self) -> str:
        chunks = []
        if self.buffer:
            chunks.append(self.buffer)
            self.buffer = b""
        while True:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
        text = b"".join(chunks).decode("utf-8", errors="replace")
        print(text, end="")
        return text

    def send_line(self, data: str):
        self.sock.sendall(data.encode("utf-8") + b"\n")


def brute_level_one(leak: str, target_hash: str) -> str:
    result = {"value": None}
    stop = threading.Event()
    workers = max(os.cpu_count() or 4, 4)
    chunk = math.ceil(len(ALPHABET) / workers)

    def worker(block: str):
        for c1 in block:
            if stop.is_set():
                return
            for c2 in ALPHABET:
                if stop.is_set():
                    return
                candidate = leak + c1 + c2
                if vibe_hash(candidate) == target_hash:
                    result["value"] = candidate
                    stop.set()
                    return

    threads = []
    for i in range(workers):
        subset = ALPHABET[i * chunk:(i + 1) * chunk]
        if not subset:
            continue
        t = threading.Thread(target=worker, args=(subset,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if not result["value"]:
        raise RuntimeError("failed level 1 brute force")
    return result["value"]


def solve_level_one(conn: Conn):
    text = conn.read_until(b"Enter password: ")
    leak = re.search(r"Leaked Note: ([A-Za-z0-9]+)", text).group(1)
    target_hash = re.search(r"Target Hash: (vb\$1\$[A-Za-z0-9+/=]+)", text).group(1)
    recovered = brute_level_one(leak, target_hash)
    conn.send_line(recovered)


def solve_level_two(conn: Conn):
    text = conn.read_until(b"Format: string1,string2")
    prefix = re.search(r"prefix: '([^']+)'", text, re.IGNORECASE).group(1)
    s1 = prefix + "A"
    s2 = s1 + ("B" * 256)
    conn.send_line(f"{s1},{s2}")


def solve_level_three(conn: Conn):
    text = conn.read_until(b"Enter the equivalent password: ")
    target_len = int(re.search(r"very long \((\d+) 'B's\)", text).group(1))
    remainder = target_len % 256
    if remainder == 0:
        remainder = 256
    conn.send_line("B" * remainder)


def solve_level_four(conn: Conn):
    text = conn.read_until(b"Enter password: ")
    pad_len = int(re.search(r"password is: (\d+) 'C's", text).group(1))
    emoji_count = int(re.search(r"\+ (\d+) '🔥'", text).group(1))
    emoji = "🔥"
    byte_budget = 72
    emoji_bytes = len(emoji.encode())
    if pad_len >= byte_budget:
        c_count = byte_budget
        emoji_to_use = 0
    else:
        c_count = pad_len
        remaining = byte_budget - pad_len
        emoji_to_use = min(emoji_count, remaining // emoji_bytes)
    candidate = ("C" * c_count) + (emoji * emoji_to_use)
    conn.send_line(candidate)


def solve_level_five(conn: Conn):
    text = conn.read_until(b"Input your password:")
    admin_pw_len = int(re.search(r"SecretPassword: (\d+) 'X'", text).group(1))
    total_len = int(re.search(r"Total Length = (\d+) bytes", text).group(1))
    wrap = total_len % 256
    prefix_len = len(PREFIX)
    chunk_len = max(wrap - prefix_len, 0)
    filler_len = (wrap - prefix_len) % 256 - chunk_len
    user_input = "X" * chunk_len + "Y" * filler_len
    conn.send_line(user_input)


def main():
    conn = Conn(HOST, PORT)
    print(f"[*] Connected to {HOST}:{PORT}")
    try:
        solve_level_one(conn)
        solve_level_two(conn)
        solve_level_three(conn)
        solve_level_four(conn)
        solve_level_five(conn)
        conn.read_all()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
