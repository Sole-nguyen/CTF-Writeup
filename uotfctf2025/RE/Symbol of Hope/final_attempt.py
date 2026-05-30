# -*- coding: utf-8 -*-
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

# Maybe the pattern is: ROR by (position % some_number) then XOR with (position)?
# Or just ROR by position!

print("Trying: ROR by position, then XOR with constant or position...")

for base_xor in range(256):
    # Try: ROR(data[i], i) ^ base_xor
    result = []
    for i in range(42):
        dec = ror(data[i], i % 8) ^ base_xor
        result.append(dec)
    
    try:
        text = bytes(result).decode('ascii')
        if text.startswith('uoftctf{'):
            print(f"\n*** Method 1: ROR(byte, pos%8) ^ 0x{base_xor:02x} ***")
            print(text)
            break
    except:
        pass

# Try: ROR(data[i], i) ^ i
result = []
for i in range(42):
    dec = ror(data[i], i % 8) ^ i
    result.append(dec)

try:
    text = bytes(result).decode('ascii')
    if text.startswith('uoftctf{'):
        print(f"\n*** Method 2: ROR(byte, pos%8) ^ pos ***")
        print(text)
except:
    pass

# Try: ROR(data[i], constant) ^ i
for ror_const in range(8):
    result = []
    for i in range(42):
        dec = ror(data[i], ror_const) ^ i
        result.append(dec)
    
    try:
        text = bytes(result).decode('ascii')
        if text.startswith('uoftctf{'):
            print(f"\n*** Method 3: ROR(byte, {ror_const}) ^ pos ***")
            print(text)
            break
    except:
        pass

# Try without ROR: just XOR with position
result = []
for i in range(42):
    dec = data[i] ^ i
    result.append(dec)

try:
    text = bytes(result).decode('ascii')
    print(f"\nMethod 4 (no ROR, XOR with pos): {repr(text)}")
    if text.startswith('uoftctf{'):
        print(f"*** THIS IS IT! ***")
        print(text)
except Exception as e:
    print(f"Method 4 failed: {e}")

# Print first few bytes to debug
print(f"\nFirst 10 bytes XOR'd with position:")
for i in range(min(10, len(data))):
    print(f"  {i}: 0x{data[i]:02x} ^ {i} = 0x{data[i]^i:02x} = '{chr(data[i]^i) if 32 <= (data[i]^i) < 127 else '?'}'")
