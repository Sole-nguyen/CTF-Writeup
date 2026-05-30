#!/usr/bin/env python3
MASK = (1 << 64) - 1


def ror(x: int, n: int) -> int:
    n &= 63
    return ((x >> n) | ((x << (64 - n)) & MASK)) & MASK


def build_tables() -> list[list[int]]:
    rdx = 0x09E7448B1D3CF26A
    r12 = 0x6C62272E07BB0142
    r8 = 0
    r9 = 0
    r10 = 0
    r13 = 0

    add_r10 = 0x9E3779B97F4A7C15
    add_r9 = 0xBF58476D1CE4E5B9
    target_r9 = 0xE08D64756AEB12B0

    blocks = []
    while True:
        r11 = 0x40 - (r13 & 0x3F)
        rcx = 0
        rsi = 0
        block = []
        for _ in range(256):
            rax = ((rdx >> 63) & 1) ^ (rdx & 1) ^ ((rdx >> 3) & 1) ^ ((rdx >> 2) & 1)
            rax = (rax + rdx + r8) & MASK
            r8 = 1 if rax < rdx else 0
            rdx = ror(rax, 0x39)

            rax = ((rcx << (r13 & 0x3F)) | (rcx >> (r11 & 0x3F))) & MASK
            rax ^= (rsi ^ r10) & MASK
            rax ^= rdx
            block.append(rax)

            rcx = (rcx + r12) & MASK
            rsi = (rsi + r9) & MASK

        blocks.append(block)
        r13 += 1
        r10 = (r10 + add_r10) & MASK
        r9 = (r9 + add_r9) & MASK
        if r9 == target_r9:
            break
    return blocks


def compute_input_hex() -> str:
    blocks = build_tables()

    r9 = 0x02 << 32
    r10 = 0x823EAF93561AD964
    r11 = 0x000000070E71C5389D
    r12 = 0xD2A98B26625EEE7B
    rbp = 0

    qwords = [
        0xF0C553137025AFD6,
        0x376DDFC434D0F4D4,
        0x04F9BDE7A77AE197,
        0x0A89E4C1254BA31B,
        0xB7C0F25B3F70D12B,
    ]
    output_bytes = b"".join(q.to_bytes(8, "little") for q in qwords)

    inp = bytearray(40)
    for i in range(40):
        idx = (r11 >> 56) & 0xFF
        table_entry = blocks[i][idx]
        inp[i] = output_bytes[i] ^ (table_entry & 0xFF)

        rdx = (r10 + r11) & MASK
        rcx = (r9 ^ rdx) & MASK
        rcx = ror(rcx, 0x38)
        rbp = (rbp + rcx) & MASK
        rax = (r10 ^ rbp) & MASK
        rax = ror(rax, 0x2D)
        rdx = (rdx + rax) & MASK
        rcx ^= rdx
        rcx = ror(rcx, 0x18)
        r9 = rcx
        rbp = (rbp + rcx) & MASK
        rdx = (rdx + rbp) & MASK
        rdx = ror(rdx, 0x25)
        r11 = rdx
        rax ^= rbp
        r10 = ror(rax, 0x1)
        r10 = (r10 * r12) & MASK
        rax = (0xAAAAAAAAAAAAAAAB * i) & MASK
        rax ^= rdx
        r10 ^= rax

    return inp.hex()


def main() -> None:
    print(compute_input_hex())


if __name__ == "__main__":
    main()
