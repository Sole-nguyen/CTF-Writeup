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

# Since binary has rol8 and ror8, plus many functions f_10...f_74 (65 functions!)
# Maybe each byte uses a different transformation?

# Let's assume the flag starts with "uoftctf{" and try to find what
# transformation each position uses

known_start = list(b"uoftctf{")
known_end = [ord('}')]

# For each position in known_start, try different operations
def try_operations(plain, cipher):
    ops = []
    # XOR with various values
    for xor_val in [0x10, 0x20, 0x30, 0x55, 0xAA]:
        if plain ^ xor_val == cipher:
            ops.append(f"XOR 0x{xor_val:02x}")
    
    # Rotations
    for n in range(1, 8):
        if ror(plain, n) == cipher:
            ops.append(f"ROR {n}")
        if rol(plain, n) == cipher:
            ops.append(f"ROL {n}")
    
    # ADD/SUB
    if (plain + 1) & 0xFF == cipher:
        ops.append("ADD 1")
    if (plain - 1) & 0xFF == cipher:
        ops.append("SUB 1")
    
    # NOT
    if (~plain) & 0xFF == cipher:
        ops.append("NOT")
    
    # Nibble swap
    if ((plain & 0x0F) << 4) | ((plain & 0xF0) >> 4) == cipher:
        ops.append("NIBBLE_SWAP")
    
    return ops if ops else ["UNKNOWN"]

print("Operations for known prefix 'uoftctf{':")
for i in range(len(known_start)):
    ops = try_operations(known_start[i], data[i])
    print(f"Position {i} ('{chr(known_start[i])}'): {', '.join(ops)}")

print(f"\nLast position (assuming '}}'):")
ops = try_operations(ord('}'), data[-1])
print(f"Position {len(data)-1}: {', '.join(ops)}")

# Try assuming it's a simple operation applied to all
# Let's try: first subtract position, then XOR with a byte, then rotate
print("\n=== Trying formula: ROR(byte ^ key, rot_amount) ===")
for rot in range(1, 8):
    for key in range(256):
        # Try: encrypted = ROR(plaintext ^ key, rot)
        # So: plaintext = (ROL(encrypted, rot)) ^ key
        result = []
        for i, enc_byte in enumerate(data):
            plain_byte = rol(enc_byte, rot) ^ key
            result.append(plain_byte)
        
        try:
            text = bytes(result).decode('ascii')
            if text.startswith('uoftctf{') and text.endswith('}'):
                print(f"\n*** FOUND! ROT={rot}, KEY=0x{key:02x} ***")
                print(text)
                exit(0)
        except:
            pass

print("\nNo simple solution found. The transformation might be per-byte or more complex.")
