#!/usr/bin/env python3
from datetime import datetime, timedelta
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    target = base / "81fea8c4-0b3b-4ce0-9258-43fd03502fb0.txt"

    with target.open("r", encoding="utf-8") as f:
        dates = [datetime.strptime(line.strip(), "%Y%m%d").date() for line in f if line.strip()]

    date_set = set(dates)
    start, end = min(date_set), max(date_set)

    missing = None
    current = start
    while current <= end:
        if current not in date_set:
            missing = current
            break
        current += timedelta(days=1)

    if missing is None:
        raise RuntimeError("No missing date found")

    print(f"cyh{{{missing.strftime('%Y%m%d')}}}")


if __name__ == "__main__":
    main()

