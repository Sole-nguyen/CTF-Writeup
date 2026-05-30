from collections import defaultdict


NUMS = [
    95, 181, 145, 39, 245, 91, 212, 232, 123, 220, 167, 69, 91, 208, 245, 164, 245, 145, 123, 94,
    62, 150, 94, 172, 83, 135, 96, 153, 2, 208, 96, 172, 201, 5, 19,
    131, 91, 90, 53, 95, 218, 238, 211, 91, 4, 201, 182, 135, 245, 167, 74, 90, 145, 96, 238,
]

# User-confirmed constraints collected during analysis.
KNOWN_32 = "maytheforcebewithyouyoungpadawan"
MOD = 27
PERIOD = 34


def digit_transform(n: int) -> int:
    # User-confirmed transform branch that was explored:
    # c = (floor(n/10) + (n % 10)) mod 27
    return ((n // 10) + (n % 10)) % MOD


def derive_partial_key():
    cvals = [digit_transform(n) for n in NUMS]
    pvals = [ord(ch) - 97 for ch in KNOWN_32]
    key = [None] * PERIOD

    for i, p in enumerate(pvals):
        key[i % PERIOD] = (cvals[i] - p) % MOD
    return cvals, key


def decrypt_body_with_partial_key() -> str:
    cvals, key = derive_partial_key()
    out = []
    for i in range(35, 55):
        kj = key[i % PERIOD]
        if kj is None:
            out.append("?")
            continue
        p = (cvals[i] - kj) % MOD
        out.append("_" if p == 26 else chr(p + 97))
    return "".join(out)


def main() -> None:
    cvals, key = derive_partial_key()
    print("c-values:", cvals)
    print("known key slots:", sum(k is not None for k in key), "/", PERIOD)
    print("partial-body:", decrypt_body_with_partial_key())

    # NOTE:
    # Despite deep brute-force, this challenge remained underconstrained
    # without a definitive final mapping detail. This script keeps the
    # reproducible analysis path and partial decryption.


if __name__ == "__main__":
    main()
