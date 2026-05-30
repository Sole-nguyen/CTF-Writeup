#!/usr/bin/env python3
from pathlib import Path

MOD = 256
TABLE_OFFSET = 0x22A0
COUNT = 0x54


def _build_sequence(a_mod: int):
    seen = {}
    seq = []
    val = a_mod
    n = 1
    while val not in seen:
        seen[val] = n
        seq.append(val)
        val = pow(a_mod, val, MOD)
        n += 1
    mu = seen[val]
    lam = n - mu
    return seq, mu, lam


_SEQ_CACHE = {}


def tetration_mod_256(a: int, b: int) -> int:
    if b == 0:
        return 1
    a_mod = a % MOD
    seq, mu, lam = _SEQ_CACHE.setdefault(a_mod, _build_sequence(a_mod))
    if b <= len(seq):
        return seq[b - 1]
    if b < mu:
        return seq[b - 1]
    idx = mu + ((b - mu) % lam)
    return seq[idx - 1]


def main() -> None:
    binary = Path(__file__).with_name("not_quite_optimal").read_bytes()
    out = []
    for i in range(COUNT):
        off = TABLE_OFFSET + i * 16
        a = int.from_bytes(binary[off : off + 8], "little")
        b = int.from_bytes(binary[off + 8 : off + 16], "little")
        r = tetration_mod_256(a, b)
        out.append(((r + 1) >> 1) & 0xFF)
    flag = bytes(out).decode()
    print(flag)


if __name__ == "__main__":
    main()
