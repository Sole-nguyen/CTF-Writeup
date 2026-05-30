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

# Hint from challenge: "Go Go Squid!" - maybe it's a key?
keys_to_try = [
    "Go Go Squid!",
    "gogosquid",
    "squid",
    "Symbol of Hope",
    "symbolofhope",
    "hope",
]

print("=== TRY XOR WITH KEYS ===")
for key in keys_to_try:
    key_bytes = key.encode()
    result = ""
    for i, byte in enumerate(data):
        result += chr(byte ^ key_bytes[i % len(key_bytes)])
    print(f"\nKey '{key}':")
    print(f"  Hex: {result.encode('latin-1').hex()}")
    print(f"  ASCII: {repr(result)}")
    if all(32 <= ord(c) < 127 for c in result):
        print(f"  *** READABLE: {result}")

print("\n=== TRY XOR WITH SINGLE BYTE ===")
for key_byte in range(256):
    result = "".join([chr(b ^ key_byte) for b in data])
    if result.startswith("uoftctf{") or "uoftctf" in result.lower():
        print(f"Key byte 0x{key_byte:02x}: {result}")

print("\n=== TRY ROR + XOR ===")
for rot in range(1, 8):
    rotated = [ror(b, rot) for b in data]
    for key_byte in range(256):
        result = "".join([chr(b ^ key_byte) for b in rotated])
        if result.startswith("uoftctf{"):
            print(f"ROR {rot} + XOR 0x{key_byte:02x}: {result}")

print("\n=== TRY ROL + XOR ===")
for rot in range(1, 8):
    rotated = [rol(b, rot) for b in data]
    for key_byte in range(256):
        result = "".join([chr(b ^ key_byte) for b in rotated])
        if result.startswith("uoftctf{"):
            print(f"ROL {rot} + XOR 0x{key_byte:02x}: {result}")

print("\n--- THỬ XOAY PHẢI (ROR) ---")
for i in range(1, 8):
    res = "".join([chr(ror(b, i)) for b in data])
    print(f"ROR {i}: {res}")

print("\n--- THỬ XOAY TRÁI (ROL) ---")
for i in range(1, 8):
    res = "".join([chr(rol(b, i)) for b in data])
    print(f"ROL {i}: {res}")