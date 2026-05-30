#!/usr/bin/env python3
import re
from pathlib import Path


def iroot3(n: int) -> int:
    lo, hi = 0, 1
    while hi**3 <= n:
        hi <<= 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    output_file = next(Path(".").glob("output.txt*"))
    text = output_file.read_text()

    values = {k: int(v) for k, v in re.findall(r"(n[123]|c[123]|e)\s*=\s*([0-9]+)", text)}
    c = values["c1"]
    e = values["e"]

    if e != 3:
        raise ValueError(f"Unexpected exponent: {e}")

    m = iroot3(c)
    if m**3 != c:
        raise ValueError("Ciphertext is not a perfect cube; Håstad precondition failed.")

    flag = m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
    print(flag)


if __name__ == "__main__":
    main()
