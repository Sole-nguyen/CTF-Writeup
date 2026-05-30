#!/usr/bin/env python3
"""
Auto-solver for Switcheroo challenge.
Run: python3 solve_flag.py
"""

from z3 import BitVec, BitVecVal, LShR, Or, Solver, ULE, sat

N = 27


def rot(arr, k):
    out = [None] * N
    for i in range(N):
        out[(i + k) % N] = arr[i]
    return out


def switch(arr, p):
    arr = arr[:]
    if p % 2 == 0:
        for i in range(p):
            arr[(i * p) % N] = arr[(i * p) % N] + BitVecVal(p, 8)
        arr = rot(arr, p)
    else:
        arr = rot(arr, p)
        for i in range(p):
            arr[(i + p) % N] = arr[(i + p) % N] - BitVecVal(p, 8)
    return arr


def half_neg_minus2(v):
    return BitVecVal(0, 8) - ((v + LShR(v, 7)) >> 1) - BitVecVal(2, 8)


def half_neg_plus8(v):
    return BitVecVal(0, 8) - ((v + LShR(v, 7)) >> 1) + BitVecVal(8, 8)


def solve_all(limit=20):
    x = [BitVec(f"x{i}", 8) for i in range(N)]
    s = Solver()

    for c in x:
        s.add(ULE(BitVecVal(0x21, 8), c), ULE(c, BitVecVal(0x7E, 8)))

    # flag wrapper
    prefix = b"texsaw{"
    for i, b in enumerate(prefix):
        s.add(x[i] == b)
    s.add(x[26] == ord("}"))

    a = x[:]
    a = switch(a, 5)
    a = switch(a, 6)
    s.add(a[11] == ord("o"))

    a = switch(a, 13)
    s.add(a[14] == ord("R"))

    a = switch(a, 3)
    a = switch(a, 24)
    s.add(a[0] == 0x9B)
    s.add(ULE(BitVecVal(0x73, 8), a[26]), ULE(a[26], BitVecVal(0x77, 8)))

    a = switch(a, 10)
    s.add(a[8] == ord("Y"))
    s.add(a[11] == ord("Y"))
    s.add(ULE(BitVecVal(0x74, 8), a[12]), ULE(a[12], BitVecVal(0x77, 8)))

    a = switch(a, 7)
    s.add(a[20] == 0xB5)
    s.add(a[13] == ord("s"))

    # "README.txt" constraints from final checker
    s.add(a[0] - 0x21 == ord("R"))
    s.add(a[1] - 0x20 == ord("E"))
    s.add(a[2] - 0x28 == ord("A"))
    s.add((a[3] + 4) * 2 == ord("D"))
    s.add(a[12] + 0x1C == ord("M"))
    s.add(a[11] - 0x66 == ord("E"))
    s.add(a[10] + 8 == ord("."))
    s.add(a[9] + 0x14 == ord("t"))
    s.add(a[8] - 7 == ord("x"))
    s.add((BitVecVal(0, 8) - (a[26] + 6)) * 2 == ord("t"))

    hexset = [ord(c) for c in "0123456789abcdefABCDEF"]

    def is_hex(ch):
        return Or(*[ch == BitVecVal(v, 8) for v in hexset])

    h1 = half_neg_minus2(a[5])
    h2 = a[6] + 4
    h3 = a[7] - 0x2B
    h4 = a[25] - 0x31
    h5 = a[24] + 5
    h6 = half_neg_plus8(a[23])
    h7 = a[22] - 0x0F
    h8 = a[21] - 0x3D

    for h in [h1, h2, h3, h4, h5, h6, h7, h8]:
        s.add(is_hex(h))

    s.add(h1 == ord("5"), h2 == ord("7"))
    s.add(h3 == ord("3"), h4 == ord("4"))
    s.add(h5 == ord("6"), h6 == ord("1"))
    s.add(h7 == ord("2"), h8 == ord("9"))

    results = []
    while len(results) < limit and s.check() == sat:
        m = s.model()
        b = bytes(m[c].as_long() for c in x)
        results.append(b.decode("latin1"))
        s.add(Or(*[c != m[c] for c in x]))
    return results


if __name__ == "__main__":
    flags = solve_all()
    if not flags:
        print("No solution found.")
    elif len(flags) == 1:
        print(flags[0])
    else:
        print("Possible flags:")
        for f in flags:
            print(f"- {f}")
        # most human-readable candidate
        prefer = "texsaw{pAt1ence!!_W0rKn0w?}"
        if prefer in flags:
            print(f"\nLikely intended: {prefer}")
