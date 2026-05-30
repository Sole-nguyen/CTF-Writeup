#!/usr/bin/env python3
import csv
import math
from pathlib import Path
from typing import List, Tuple


def read_samples(csv_path: Path) -> Tuple[List[float], List[int]]:
    times: List[float] = []
    levels: List[int] = []
    with csv_path.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            if len(row) < 2:
                continue
            times.append(float(row[0]))
            levels.append(1 if row[1].strip() == "1" else 0)
    return times, levels


def decode_uart(levels: List[int], dt: float, baud: float, phase: float) -> Tuple[bytes, float, float]:
    bit_samples = (1.0 / baud) / dt
    if bit_samples <= 0:
        return b"", 0.0, 0.0

    out = bytearray()
    valid_stop = 0
    i = 1
    max_index = len(levels) - int(math.ceil(10 * bit_samples)) - 2
    while i < max_index:
        if levels[i - 1] == 1 and levels[i] == 0:
            start = i
            val = 0
            for bit in range(8):
                sample_index = int(round(start + (phase + bit) * bit_samples))
                if 0 <= sample_index < len(levels) and levels[sample_index]:
                    val |= 1 << bit
            stop_index = int(round(start + (phase + 8) * bit_samples))
            if 0 <= stop_index < len(levels) and levels[stop_index] == 1:
                valid_stop += 1
            out.append(val)
            i = int(round(start + 10 * bit_samples))
            continue
        i += 1

    printable = sum(
        1 for b in out if (32 <= b <= 126) or b in (9, 10, 13)
    )
    total = len(out) if out else 1
    printable_ratio = printable / total
    stop_ratio = valid_stop / total
    return bytes(out), printable_ratio, stop_ratio


def find_best_decode(levels: List[int], dt: float) -> Tuple[bytes, float]:
    sample_rate = 1.0 / dt
    common_bauds = [
        110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800,
        31250, 32000, 33333, 38400, 57600, 115200,
    ]
    candidates = set(common_bauds)
    approx = int(round(sample_rate))
    for b in range(max(300, approx - 5000), approx + 5001, 100):
        candidates.add(b)

    best_score = -1.0
    best_bytes = b""
    best_baud = 0.0
    for baud in sorted(candidates):
        for phase in [x / 100.0 for x in range(100, 201, 5)]:  # 1.00..2.00
            decoded, printable_ratio, stop_ratio = decode_uart(levels, dt, baud, phase)
            score = printable_ratio * 0.7 + stop_ratio * 0.3
            if score > best_score:
                best_score = score
                best_bytes = decoded
                best_baud = baud
    return best_bytes, best_baud


def extract_flag(text: str) -> str:
    marker = "secretflag:"
    if marker in text:
        after = text.split(marker, 1)[1].strip()
        hex_str = after.split()[0]
        try:
            return bytes.fromhex(hex_str).decode("ascii", errors="replace")
        except ValueError:
            pass
    # Fallback: search for hex-looking tokens
    for token in text.split():
        if all(c in "0123456789abcdefABCDEF" for c in token) and len(token) >= 8:
            try:
                return bytes.fromhex(token).decode("ascii", errors="replace")
            except ValueError:
                continue
    return ""


def main() -> None:
    csv_path = Path(__file__).with_name("code.csv")
    times, levels = read_samples(csv_path)
    if len(times) < 2:
        raise SystemExit("Not enough samples")
    dt = times[1] - times[0]
    decoded, baud = find_best_decode(levels, dt)
    text = decoded.decode("latin-1", errors="replace")
    flag = extract_flag(text)
    print(f"Detected baud: {baud}")
    if flag:
        print(flag)
    else:
        print("Flag not found")


if __name__ == "__main__":
    main()
