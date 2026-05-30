#!/usr/bin/env python3
import re
from pathlib import Path

from PIL import Image


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    target = base / "212fdea2-5eba-460e-b01c-8f4cc3f1b73e.png"

    img = Image.open(target).convert("RGB")
    pixels = img.load()
    width, height = img.size

    bits = []
    for y in range(height):
        for x in range(width):
            b = pixels[x, y][2]
            bits.append(b & 1)

    raw = bytearray()
    for i in range(0, len(bits) - 7, 8):
        value = 0
        for bit in bits[i : i + 8]:
            value = (value << 1) | bit
        raw.append(value)

    match = re.search(rb"grodno\{[^}]+\}", raw)
    if not match:
        raise RuntimeError("Flag not found in PNG blue-channel LSB stream")

    print(match.group(0).decode("ascii"))


if __name__ == "__main__":
    main()

