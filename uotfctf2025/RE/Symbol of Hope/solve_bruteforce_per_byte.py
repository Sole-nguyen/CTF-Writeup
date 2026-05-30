# -*- coding: utf-8 -*-
"""
Since each byte is transformed by a different function in the binary,
we can brute force each position independently!

For each byte position:
- Try all 256 possible input values
- Apply common transformations
- See which one matches the expected encrypted value
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

# Generate all possible transformation functions
def get_transforms(position):
    """Generate transformations that might be used for this position"""
    transforms = []
    
    # XOR with various values
    for xor_val in range(256):
        transforms.append(('xor', xor_val, lambda b, x=xor_val: b ^ x))
    
    # ROL/ROR with various amounts
    for n in range(1, 8):
        transforms.append(('ror', n, lambda b, r=n: ror(b, r)))
        transforms.append(('rol', n, lambda b, r=n: rol(b, r)))
    
    # NOT
    transforms.append(('not', 0, lambda b: (~b) & 0xFF))
    
    # ADD/SUB
    for val in range(256):
        transforms.append(('add', val, lambda b, v=val: (b + v) & 0xFF))
        transforms.append(('sub', val, lambda b, v=val: (b - v) & 0xFF))
    
    return transforms

print("Brute forcing each byte position independently...")
print("(Looking for printable ASCII 0x20-0x7E)\n")

flag_bytes = []

for pos in range(42):
    expected = data[pos]
    candidates = []
    
    # Try all printable ASCII characters
    for plaintext in range(0x20, 0x7F):  # Printable ASCII
        # Try simple transformations first
        transforms_to_try = [
            ('xor_pos', plaintext ^ pos),
            ('xor_0x10', plaintext ^ 0x10),
            ('ror_pos', ror(plaintext, pos % 8)),
            ('rol_pos', rol(plaintext, pos % 8)),
            ('add_pos', (plaintext + pos) & 0xFF),
            ('not', (~plaintext) & 0xFF),
        ]
        
        for name, result in transforms_to_try:
            if result == expected:
                candidates.append((chr(plaintext), name))
                break
    
    if len(candidates) == 1:
        flag_bytes.append(candidates[0][0])
        print(f"Pos {pos:2d}: '{candidates[0][0]}' (via {candidates[0][1]})")
    elif len(candidates) > 1:
        # Multiple candidates - prefer based on context
        if pos < 8:
            # Should be "uoftctf{"
            expected_chars = "uoftctf{"
            if expected_chars[pos] in [c[0] for c in candidates]:
                flag_bytes.append(expected_chars[pos])
                print(f"Pos {pos:2d}: '{expected_chars[pos]}' (matched prefix)")
            else:
                flag_bytes.append(candidates[0][0])
                print(f"Pos {pos:2d}: '{candidates[0][0]}' (first of {len(candidates)} candidates)")
        elif pos == 41:
            # Should be "}"
            if '}' in [c[0] for c in candidates]:
                flag_bytes.append('}')
                print(f"Pos {pos:2d}: '}}' (matched suffix)")
            else:
                flag_bytes.append(candidates[0][0])
                print(f"Pos {pos:2d}: '{candidates[0][0]}' (first of {len(candidates)} candidates)")
        else:
            flag_bytes.append(candidates[0][0])
            print(f"Pos {pos:2d}: '{candidates[0][0]}' ({len(candidates)} candidates)")
    else:
        flag_bytes.append('?')
        print(f"Pos {pos:2d}: '?' (no simple match)")

flag = ''.join(flag_bytes)
print(f"\n{'='*60}")
print(f"Potential flag: {flag}")
print(f"{'='*60}")

if flag.startswith('uoftctf{') and flag.endswith('}'):
    print("\n✓ Flag format looks correct!")
else:
    print("\n⚠ Flag format doesn't match - may need deeper analysis")
