# -*- coding: utf-8 -*-
"""
Based on the assembly analysis:
f_10 processes byte at offset 0x1E (30) and subtracts 0x67

To decrypt, we need to do the INVERSE operation:
- If encrypt did: byte -= 0x67
- Then decrypt does: byte += 0x67

Let's test this theory on position 30:
"""

data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

print("Testing f_10 logic on position 30:")
print(f"Encrypted byte at pos 30: 0x{data[30]:02x} ({data[30]})")
print(f"Decrypted (add 0x67): 0x{(data[30] + 0x67) & 0xFF:02x} = '{chr((data[30] + 0x67) & 0xFF)}'")

print("\n" + "="*60)
print("To fully solve this, you need to:")
print("1. Analyze each function f_0, f_10, f_11, ... f_74")
print("2. Find which position each function processes")
print("3. Find what operation each function does (sub, add, xor, rol, ror)")
print("4. Apply the INVERSE operation to decrypt")
print("="*60)

print("\nIn IDA, you can:")
print("- Double-click on f_11, f_12, etc. to see their code")
print("- Look for the 'add rax, XXh' instruction - this tells you the position")
print("- Look for sub/add/xor instructions - this tells you the operation")
print("\nOr use a script to extract all function info!")
