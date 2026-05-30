#!/usr/bin/env python3
from pwn import *

context.log_level = 'warn'

# Test different format specifiers
formats_to_test = [
    b"%p",
    b"%s", 
    b"%d",
    b"%x",
    b"%llx",
    b"%ld",
    b"%lx",
]

for fmt in formats_to_test:
    try:
        p = process('./app')
        p.recvuntil(b"Write your path:")
        p.sendline(fmt)
        response = p.recvall(timeout=1)
        print(f"{fmt.decode():10s} -> {response[:100]}")
        p.close()
    except:
        print(f"{fmt.decode():10s} -> ERROR")
