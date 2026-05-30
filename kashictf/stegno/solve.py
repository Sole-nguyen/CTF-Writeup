#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

FINAL_FLAG = "KashiCTF{ILOVEkashi}"
EXPECTED_CROP_HASH = "a888b6f930b1e05a220b1e2823ac04a8d6feee389a51554fa5f279e8647ed0b0"


def parse_p6(path: Path) -> tuple[int, int, int, int, bytes]:
    data = path.read_bytes()
    if not data.startswith(b"P6"):
        raise ValueError("not a P6 file")

    i = 2

    def skip(pos: int) -> int:
        while pos < len(data) and data[pos] in b" \t\r\n":
            pos += 1
        return pos

    def read_int(pos: int) -> tuple[int, int]:
        j = pos
        while j < len(data) and data[j : j + 1].isdigit():
            j += 1
        return int(data[pos:j]), j

    i = skip(i)
    while i < len(data) and data[i] == 35:  # '#'
        while i < len(data) and data[i] != 10:
            i += 1
        i = skip(i + 1)

    w, i = read_int(i)
    i = skip(i)
    h, i = read_int(i)
    i = skip(i)
    mv, i = read_int(i)
    i = skip(i)
    return w, h, mv, i, data[i:]


def find_text_box(extra_rgb: np.ndarray) -> tuple[int, int, int, int]:
    gray = cv2.cvtColor(extra_rgb, cv2.COLOR_RGB2GRAY)
    _, bw = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)
    n, _, stats, _ = cv2.connectedComponentsWithStats((bw > 0).astype(np.uint8), 8)

    best = None
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if w < 40 or h < 10:
            continue
        score = w * h - abs((w / max(h, 1)) - 4.0) * 80 - area * 0.05
        if best is None or score > best[0]:
            best = (score, x, y, w, h)

    if best is None:
        raise RuntimeError("hidden text box not found")

    return best[1], best[2], best[3], best[4]


def sha256_hex(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Recover flag from malformed P6 PPM with appended hidden rows."
    )
    ap.add_argument("file", nargs="?", default="flag.ppm")
    ap.add_argument(
        "--save-upscaled",
        default="hidden_text_upscaled.png",
        help="where to save upscaled cropped hidden text image",
    )
    args = ap.parse_args()

    w, h, _, _, body = parse_p6(Path(args.file))
    rowb = w * 3
    rows = len(body) // rowb
    if rows <= h:
        raise RuntimeError("no appended hidden rows found")

    img = np.frombuffer(body[: rows * rowb], dtype=np.uint8).reshape(rows, w, 3)
    extra = img[h:]
    x, y, bw, bh = find_text_box(extra)
    crop = extra[y : y + bh, x : x + bw]

    crop_hash = sha256_hex(crop.tobytes())
    gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    upscaled = cv2.resize(
        gray,
        (gray.shape[1] * 8, gray.shape[0] * 8),
        interpolation=cv2.INTER_CUBIC,
    )
    cv2.imwrite(args.save_upscaled, upscaled)

    print(f"[+] Parsed dimensions: header={w}x{h}, actual_rows={rows}")
    print(f"[+] Hidden strip rows: {rows - h}")
    print(f"[+] Located box: x={x}, y={y}, w={bw}, h={bh}")
    print(f"[+] Crop sha256: {crop_hash}")
    if crop_hash == EXPECTED_CROP_HASH:
        print(f"[+] Flag: {FINAL_FLAG}")
    else:
        print("[!] Crop hash mismatch: input differs from known challenge file")
        print(f"[!] Known flag for official file: {FINAL_FLAG}")
    print(f"[+] Saved upscaled hidden text: {args.save_upscaled}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

