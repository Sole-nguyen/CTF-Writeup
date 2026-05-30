#!/usr/bin/env python3
from pwn import *

context.log_level = 'warn'

# Based on the validator, let's try different combinations
test_payloads = [
    b"AAAA%c",
    b"test",
    b"%c%c",
    b"%c%c%c%c",
    b"A" * 8,
]

for payload in test_payloads:
    try:
        p = process('./app')
        p.recvuntil(b"Write your path:")
        p.sendline(payload)
        response = p.recvall(timeout=1)
        status = "OK" if b"malformed" not in response else "BLOCKED"
        print(f"{status:8s} | {payload[:20].decode(errors='ignore'):20s} | {response[:80]}")
        p.close()
    except:
        pass
