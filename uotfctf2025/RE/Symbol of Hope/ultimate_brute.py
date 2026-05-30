# -*- coding: utf-8 -*-
"""
Ultimate brute force - try complex multi-step transformations
"""
data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

def ror(val, n):
    return ((val >> n) | (val << (8 - n))) & 0xFF

def rol(val, n):
    return ((val << n) | (val >> (8 - n))) & 0xFF

# Given that there are functions f_10 through f_74 (65 functions), and 42 bytes,
# maybe it's applying 1-2 functions per byte in some pattern

# Let me try: each byte gets ROL/ROR by (position + offset) and then XOR
print("Trying various position-dependent transformations...")

for offset in range(10):
    for xor_base in range(256):
        # Try ROL by (i + offset) % 8, then XOR with xor_base
        result = []
        for i in range(42):
            dec = rol(data[i], (i + offset) % 8) ^ xor_base
            result.append(dec)
        
        try:
            text = bytes(result).decode('ascii')
            if text.startswith('uoftctf{') and text.endswith('}'):
                print(f"*** FOUND: ROL((i+{offset})%8) ^ 0x{xor_base:02x} ***\n{text}")
                exit(0)
        except:
            pass

# Try complex: ROR by position, XOR with position, then ROL
for ror_amt in range(8):
    for rol_amt in range(8):
        result = []
        for i in range(42):
            temp = ror(data[i], (i * ror_amt) % 8)
            temp = temp ^ i
            dec = rol(temp, (i * rol_amt) % 8)
            result.append(dec)
        
        try:
            text = bytes(result).decode('ascii')
            if text.startswith('uoftctf{'):
                print(f"*** FOUND complex: ROR, XOR pos, ROL ***\n{text}")
                exit(0)
        except:
            pass

# Maybe NOT is involved
result = []
for i in range(42):
    dec = (~data[i]) & 0xFF
    result.append(dec)

try:
    text = bytes(result).decode('ascii')
    print(f"NOT only: {repr(text[:20])}")
    if text.startswith('uoftctf{'):
        print(f"*** FOUND with NOT ***\n{text}")
        exit(0)
except:
    pass

# Try NOT then XOR
for xor_val in range(256):
    result = []
    for i in range(42):
        dec = (~data[i] & 0xFF) ^ xor_val
        result.append(dec)
    
    try:
        text = bytes(result).decode('ascii')
        if text.startswith('uoftctf{'):
            print(f"*** FOUND: NOT ^ 0x{xor_val:02x} ***\n{text}")
            exit(0)
    except:
        pass

print("\nStill no flag... The encryption must be very complex or use custom operations.")
print("You may need to reverse engineer the binary more deeply using IDA/Ghidra.")
