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

# Comprehensive check - try all 256 single-byte XOR values and look for readable output
print("Searching all 256 XOR keys for readable text...")
for key in range(256):
    result = bytes([b ^ key for b in data])
    try:
        text = result.decode('ascii', errors='strict')
        # Check if it looks like a flag
        if 'uoftctf{' in text.lower():
            print(f"\n*** POSSIBLE FLAG with XOR key 0x{key:02x} ***")
            print(text)
        # Or if it's mostly printable
        elif all(32 <= ord(c) < 127 or c == '\n' for c in text) and 'uoftctf' not in text.lower():
            if len([c for c in text if c.isalnum()]) > 30:
                print(f"Readable with key 0x{key:02x}: {text[:50]}...")
    except:
        pass

# Try all ROL/ROR + XOR combinations  
print("\nTrying ROL/ROR + XOR combinations...")
for rot_func, rot_name in [(rol, 'ROL'), (ror, 'ROR')]:
    for rot_amount in range(1, 8):
        for key in range(256):
            result = bytes([rot_func(b, rot_amount) ^ key for b in data])
            try:
                text = result.decode('ascii', errors='strict')
                if text.startswith('uoftctf{') and text.endswith('}'):
                    print(f"\n*** FOUND FLAG: {rot_name}{rot_amount} + XOR 0x{key:02x} ***")
                    print(text)
                    exit(0)
            except:
                pass

# Try XOR then ROL/ROR
print("\nTrying XOR + ROL/ROR combinations...")
for key in range(256):
    xored = [b ^ key for b in data]
    for rot_func, rot_name in [(rol, 'ROL'), (ror, 'ROR')]:
        for rot_amount in range(1, 8):
            result = bytes([rot_func(b, rot_amount) for b in xored])
            try:
                text = result.decode('ascii', errors='strict')
                if text.startswith('uoftctf{') and text.endswith('}'):
                    print(f"\n*** FOUND FLAG: XOR 0x{key:02x} + {rot_name}{rot_amount} ***")
                    print(text)
                    exit(0)
            except:
                pass

print("\nNo flag found with simple operations.")
