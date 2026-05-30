#!/usr/bin/env python3

import argparse
import re
import socket


def recv_until(sock: socket.socket, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def parse_macs(text: str) -> tuple[bytes, bytes]:
    m_hello = re.search(r"MAC\('hello_world'\) = ([0-9a-fA-F]{32})", text)
    m_flag = re.search(r"MAC\('get_flag'\) = ([0-9a-fA-F]{32})", text)
    if not m_hello or not m_flag:
        raise ValueError("Could not parse MAC leaks from server output.")
    return bytes.fromhex(m_hello.group(1)), bytes.fromhex(m_flag.group(1))


def build_forgery(mac_hello: bytes, mac_flag: bytes) -> tuple[str, str]:
    block1 = b"hello_world" + b"\x00" * (16 - len(b"hello_world"))
    target_block = b"get_flag" + b"\x00" * (16 - len(b"get_flag"))
    forged_block2 = bytes(x ^ y for x, y in zip(target_block, mac_hello))
    forged_msg = (block1 + forged_block2).hex()
    forged_mac = mac_flag.hex()
    return forged_msg, forged_mac


def solve(host: str, port: int, timeout: float) -> str:
    with socket.create_connection((host, port), timeout=timeout) as sock:
        banner = recv_until(sock, b"Your Message (hex)> ")
        banner_text = banner.decode(errors="ignore")
        mac_hello, mac_flag = parse_macs(banner_text)
        forged_msg, forged_mac = build_forgery(mac_hello, mac_flag)

        sock.sendall((forged_msg + "\n").encode())
        recv_until(sock, b"Your MAC (hex)> ")
        sock.sendall((forged_mac + "\n").encode())

        response = recv_until(sock, b"\n").decode(errors="ignore")
        if "flag" in response.lower():
            return response.strip()

        # Read extra output in case server sends multiple lines.
        tail = sock.recv(4096).decode(errors="ignore")
        return (response + tail).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve CBC-MAC forgery challenge.")
    parser.add_argument("--host", default="95.111.234.103", help="Challenge host")
    parser.add_argument("--port", type=int, default=1337, help="Challenge port")
    parser.add_argument("--timeout", type=float, default=15.0, help="Socket timeout")
    args = parser.parse_args()

    result = solve(args.host, args.port, args.timeout)
    print(result)


if __name__ == "__main__":
    main()
