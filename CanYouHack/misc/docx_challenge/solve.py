#!/usr/bin/env python3
import re
import zipfile
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    target = base / "189ea546-6e94-4be1-bd56-a98e5ef0c409.docx"

    with zipfile.ZipFile(target, "r") as zf:
        data = zf.read("Thumbnails/thumbnail.png")

    match = re.search(rb"grodno\{[^}]+\}", data)
    if not match:
        raise RuntimeError("Flag not found in DOCX thumbnail payload")

    print(match.group(0).decode("ascii"))


if __name__ == "__main__":
    main()

