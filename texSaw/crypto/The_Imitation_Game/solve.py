#!/usr/bin/env python3
import string
from pathlib import Path


ALPH = string.ascii_lowercase
A2I = {c: i for i, c in enumerate(ALPH)}


def only_letters(s: str) -> str:
    return "".join(ch.lower() for ch in s if ch.isalpha())


def find_period(deltas: list[int]) -> int:
    for p in range(1, len(deltas) + 1):
        if all(deltas[i] == deltas[i % p] for i in range(len(deltas))):
            return p
    raise ValueError("No period found")


def build_key_relative_constants(deltas: list[int], L: int, n_mod: int) -> list[int]:
    c = [None] * L
    c[0] = 0
    changed = True
    while changed:
        changed = False
        for r in range(L):
            if c[r] is None:
                continue
            nxt = (r + n_mod) % L
            v = (c[r] + deltas[r]) % 26
            if c[nxt] is None:
                c[nxt] = v
                changed = True
            elif c[nxt] != v:
                raise ValueError("Inconsistent key relation")
    if any(v is None for v in c):
        raise ValueError("Could not determine full key relations")
    return c  # type: ignore[return-value]


def decrypt_with_key(ciphertext: str, key: list[int]) -> str:
    out = []
    j = 0
    L = len(key)
    for ch in ciphertext:
        if ch.isalpha():
            p = (A2I[ch.lower()] - key[j % L]) % 26
            dec = ALPH[p]
            out.append(dec.upper() if ch.isupper() else dec)
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def score_english(text: str) -> float:
    t = " " + "".join(ch.lower() if ch.isalpha() else " " for ch in text) + " "
    common = [
        " the ",
        " and ",
        " to ",
        " of ",
        " that ",
        " is ",
        " in ",
        " it ",
        " you ",
        " for ",
        " on ",
        " with ",
        " as ",
        " be ",
        " this ",
        " have ",
        " are ",
        " not ",
        " they ",
    ]
    return sum(t.count(w) for w in common)


def parse_blocks(raw: str) -> tuple[str, str]:
    blocks = [b.strip("\n") for b in raw.strip("\n").split("\n\n") if b.strip()]
    if len(blocks) < 6:
        raise ValueError("Unexpected ciphertext format")

    # Structure:
    # 1) first encrypted flag
    # 2) first encrypted letter body
    # 3) first encrypted P.S. + signature
    # 4) second encrypted flag
    # 5) second encrypted letter body
    # 6) second encrypted P.S. + signature
    flag1 = blocks[0].strip()
    letter1 = blocks[1] + "\n\n" + blocks[2]
    flag2 = blocks[3].strip()
    letter2 = blocks[4] + "\n\n" + blocks[5]

    copy1 = flag1 + "\n" + letter1
    copy2 = flag2 + "\n" + letter2
    return copy1, copy2


def main() -> None:
    data = Path("ciphertext.txt").read_text(encoding="utf-8")
    copy1, copy2 = parse_blocks(data)

    l1 = only_letters(copy1)
    l2 = only_letters(copy2)
    if len(l1) != len(l2):
        raise ValueError("Copies do not align")

    deltas = [(A2I[b] - A2I[a]) % 26 for a, b in zip(l1, l2)]
    L = find_period(deltas)
    n_mod = len(l1) % L
    rel = build_key_relative_constants(deltas[:L], L, n_mod)

    best = None
    for k0 in range(26):
        key = [(k0 + v) % 26 for v in rel]
        plain = decrypt_with_key(copy1, key)
        s = score_english(plain)
        if best is None or s > best[0]:
            best = (s, plain)

    assert best is not None
    plaintext = best[1]
    flag = plaintext.splitlines()[0].strip()
    print(flag)


if __name__ == "__main__":
    main()
