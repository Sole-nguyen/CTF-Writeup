#!/usr/bin/env python3
from itertools import product
import subprocess
from pathlib import Path

BASE = 0x83
LEN_PER_BUCKET = 8
TARGETS = [
    0x00FD91B66D4B8B11,
    0x00E661491544FDB8,
    0x010FC69E6442EF55,
    0x00F680346B31A222,
]


def reverse_bucket(target: int) -> list[list[int]]:
    sols: list[list[int]] = []

    def dfs(h: int, steps_left: int, suffix: list[int]) -> None:
        if steps_left == 0:
            if 0 <= h <= 0xFF:
                sols.append([h] + suffix)
            return
        r = h % BASE
        for c in (r, r + BASE):
            if 0 <= c <= 0xFF and h >= c and (h - c) % BASE == 0:
                dfs((h - c) // BASE, steps_left - 1, [c] + suffix)

    dfs(target, LEN_PER_BUCKET - 1, [])
    return sols


def recover_flag() -> str:
    bucket_texts: list[list[str]] = []
    for t in TARGETS:
        printable = []
        for cand in reverse_bucket(t):
            if all(32 <= b < 127 for b in cand):
                printable.append("".join(map(chr, cand)))
        if not printable:
            raise RuntimeError("No printable solution for a bucket")
        bucket_texts.append(printable)

    candidates = []
    for parts in product(*bucket_texts):
        out = ["?"] * 32
        for bucket_idx, part in enumerate(parts):
            for i, ch in enumerate(part):
                out[bucket_idx + 4 * i] = ch
        s = "".join(out)
        if s.startswith("kashi{") and s.endswith("}"):
            candidates.append(s)

    if len(candidates) != 1:
        raise RuntimeError(f"Expected unique flag candidate, got {len(candidates)}")
    return candidates[0]


def main() -> None:
    real_flag = recover_flag()
    submit_flag = "kashiCTF{" + real_flag[len("kashi{") : -1] + "}"
    print(f"[+] Recovered (binary output): {real_flag}")
    print(f"[+] Submission format      : {submit_flag}")

    prog = Path("prog")
    if prog.exists() and prog.is_file():
        try:
            out = subprocess.check_output([f"./{prog.name}", real_flag], text=True)
            print("[+] Binary says:")
            print(out.strip())
        except Exception as exc:
            print(f"[-] Could not run ./prog: {exc}")


if __name__ == "__main__":
    main()
