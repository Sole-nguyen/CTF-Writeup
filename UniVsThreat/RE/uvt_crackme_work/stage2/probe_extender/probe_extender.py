#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from pathlib import Path


def shannon_entropy(b: bytes) -> float:
    if not b:
        return 0.0
    counts = [0] * 256
    for x in b:
        counts[x] += 1
    n = len(b)
    ent = 0.0
    for c in counts:
        if c == 0:
            continue
        p = c / n
        ent -= p * math.log2(p)
    return ent


def find_islands(data: bytes, min_len: int = 4) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    i = 0
    n = len(data)
    while i < n:
        if data[i] == 0:
            i += 1
            continue
        j = i
        while j < n and data[j] != 0:
            j += 1
        if j - i >= min_len:
            out.append((i, j - i))
        i = j
    return out


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <file>")
        raise SystemExit(2)
    p = Path(sys.argv[1])
    data = p.read_bytes()
    print(f"file: {p} ({len(data)} bytes)")
    islands = find_islands(data)
    if not islands:
        print("no non-zero islands found")
        return
    print(f"islands: {len(islands)}")
    for off, ln in islands[:32]:
        b = data[off : off + ln]
        ent = shannon_entropy(b)
        sample = b[:16].hex()
        print(f"  off=0x{off:08x} len={ln:5d} entropy={ent:0.2f} sample={sample}")


if __name__ == "__main__":
    main()

