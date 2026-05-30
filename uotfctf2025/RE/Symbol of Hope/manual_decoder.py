# -*- coding: utf-8 -*-
"""
Manual decoder - fill in the operations from IDA analysis

For each function f_X:
1. Find the offset it processes (look for 'add rax, XXh')
2. Find the operation (sub/add/xor/rol/ror and the value)
3. Fill in the dictionary below

Example from f_10:
    add rax, 1Eh        -> processes position 0x1E (30)
    sub edx, 67h        -> subtracts 0x67
    
So to decrypt: position 30 needs ADD 0x67 (inverse of SUB)
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

# Fill this dictionary with info from IDA
# Format: position -> (operation, value)
# Operations: 'add', 'sub', 'xor', 'rol', 'ror'
decrypt_ops = {
    # Example: if f_10 does: byte[30] -= 0x67
    # Then to decrypt: byte[30] += 0x67
    # So we write: 30: ('add', 0x67)
    
    30: ('add', 0x67),  # From f_10 analysis
    
    # TODO: Fill in the rest by analyzing f_0, f_11, f_12, etc. in IDA
    # For each function:
    # 1. Find 'add rax, XXh' to get position
    # 2. Find operation (sub/add/xor/rol/ror) and value
    # 3. Add INVERSE operation here
}

print("Current decrypt operations configured:")
for pos in sorted(decrypt_ops.keys()):
    op, val = decrypt_ops[pos]
    print(f"  Position {pos:2d}: {op} 0x{val:02x}")

print("\nTo complete the solution:")
print("1. In IDA, go through f_0, f_11, f_12, ... f_74")
print("2. For each, note the position (from 'add rax, XXh')")
print("3. Note the operation (from sub/add/xor/rol/ror instruction)")
print("4. Add the INVERSE operation to decrypt_ops above")
print("\nInverse operations:")
print("  - If encrypt does SUB -> decrypt does ADD")
print("  - If encrypt does ADD -> decrypt does SUB")
print("  - If encrypt does XOR -> decrypt does XOR (same)")
print("  - If encrypt does ROL -> decrypt does ROR")
print("  - If encrypt does ROR -> decrypt does ROL")

# Try to decrypt with current ops
result = list(data)
for pos, (op, val) in decrypt_ops.items():
    if op == 'add':
        result[pos] = (result[pos] + val) & 0xFF
    elif op == 'sub':
        result[pos] = (result[pos] - val) & 0xFF
    elif op == 'xor':
        result[pos] = result[pos] ^ val
    elif op == 'rol':
        result[pos] = rol(result[pos], val)
    elif op == 'ror':
        result[pos] = ror(result[pos], val)

try:
    partial_flag = bytes(result).decode('latin-1')
    print(f"\nPartial decryption: {repr(partial_flag)}")
except:
    print(f"\nPartial decryption failed")

# Check positions we know
known = {0: 'u', 1: 'o', 2: 'f', 3: 't', 4: 'c', 5: 't', 6: 'f', 7: '{', 41: '}'}
print("\nVerification against known prefix 'uoftctf{' and suffix '}':")
for pos, expected_char in known.items():
    if pos < len(result):
        actual = chr(result[pos]) if 32 <= result[pos] < 127 else '?'
        match = "✓" if actual == expected_char else "✗"
        print(f"  Pos {pos:2d}: expected '{expected_char}', got '{actual}' {match}")
