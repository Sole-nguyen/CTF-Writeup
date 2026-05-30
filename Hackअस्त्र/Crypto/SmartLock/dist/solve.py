#!/usr/bin/env python3
import hashlib
import hmac
import json
import re
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "challenges.ctf.hackastra.tech"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 30346

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
key_size = (q.bit_length() + 7) // 8

def hval(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % q

def inv(n: int) -> int:
    return pow(n % q, -1, q)

def badge_code(ticket: str) -> int:
    value = hval(("badge-seed:" + ticket).encode())
    return value or 1

def recv_until(sock, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def send_line(sock, line: str):
    sock.sendall(line.encode() + b"\n")

with socket.create_connection((HOST, PORT), timeout=10) as sock:
    print(recv_until(sock, b"> ").decode(errors="replace"), end="")

    send_line(sock, "badge")
    print(recv_until(sock, b"name: ").decode(errors="replace"), end="")
    send_line(sock, "pwn")

    badge_out = recv_until(sock, b"> ").decode(errors="replace")
    print(badge_out, end="")

    badge = json.loads(next(line for line in badge_out.splitlines() if line.startswith("{")))
    msg = badge["msg"].encode()
    ticket = badge["ticket"]
    r = int(badge["r"], 16)
    s = int(badge["s"], 16)

    code = badge_code(ticket)
    secret = ((s * code - hval(msg)) * inv(r)) % q
    print(f"[+] recovered secret = {hex(secret)}")

    send_line(sock, "pub")
    pub_out = recv_until(sock, b"> ").decode(errors="replace")
    print(pub_out, end="")
    pub = json.loads(next(line for line in pub_out.splitlines() if line.startswith("{")))

    assert pow(g, secret, p) == int(pub["y"], 16)
    print("[+] secret verified")

    send_line(sock, "unlock")
    unlock_out = recv_until(sock, b"seal: ").decode(errors="replace")
    print(unlock_out, end="")

    nonce_hex = re.search(r"nonce: ([0-9a-f]+)", unlock_out).group(1)
    nonce = bytes.fromhex(nonce_hex)

    key = secret.to_bytes(key_size, "big")
    seal = hmac.new(key, b"unlock:" + nonce, hashlib.sha256).hexdigest()

    print(f"[+] sending seal = {seal}")
    send_line(sock, seal)

    print(recv_until(sock, b"> ").decode(errors="replace"), end="")