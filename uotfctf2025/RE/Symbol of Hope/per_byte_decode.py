# -*- coding: utf-8 -*-
"""
What if the encrypted data does NOT represent the flag format "uoftctf{...}"?
Maybe it's different encoding - let's try to find ANY printable ASCII that makes sense.
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

# Based on the function names in the binary (f_10 to f_74), there are 65 functions
# But we have 42 bytes - maybe it's using some subset?

# Let me try a different approach: What if each POSITION uses a DIFFERENT rotation/XOR?
# Try all combinations where each byte can be independently ROR'd and XOR'd

print("Trying per-byte variable operations...")
print("This will try different ROR amounts for first few bytes...")

# Let's try assuming first 8 bytes spell "uoftctf{"
target_start = list(b"uoftctf{")

# For each byte, find which (ROR, XOR) combination gives the target
solutions = []
for i in range(8):
    encrypted = data[i]
    plain = target_start[i]
    
    # Try all ROR + XOR combinations
    for ror_amount in range(8):
        for xor_key in range(256):
            # Try: plain = ROR(encrypted, ror_amount) ^ xor_key
            if (ror(encrypted, ror_amount) ^ xor_key) == plain:
                solutions.append((i, ror_amount, xor_key))
                print(f"Byte {i} ('{chr(plain)}'): ROR{ror_amount} ^ 0x{xor_key:02x}")
                break

# Now let me check if there's a pattern
if len(solutions) == 8:
    print("\nFound operations for all 8 bytes! Checking pattern...")
    
    # Check if XOR key or ROR amount follows a pattern
    ror_amounts = [s[1] for s in solutions]
    xor_keys = [s[2] for s in solutions]
    
    print(f"ROR amounts: {ror_amounts}")
    print(f"XOR keys: {[f'0x{k:02x}' for k in xor_keys]}")
    
    # Try to extrapolate the pattern to all 42 bytes
    # Simple patterns to check:
    # 1. Incrementing ROR amount
    # 2. Constant ROR amount
    # 3. ROR amount = position % 8
    
    for pattern_name, ror_pattern in [
        ("Constant", [ror_amounts[0]] * 42),
        ("Cycling", [ror_amounts[i % 8] for i in range(42)]),
        ("Position % 8", [i % 8 for i in range(42)]),
        ("Incrementing", [i % 8 for i in range(42)]),
    ]:
        for xor_pattern_name, xor_pattern in [
            ("Constant", [xor_keys[0]] * 42),
            ("Cycling", [xor_keys[i % 8] for i in range(42)]),
            ("Position", [i for i in range(42)]),
        ]:
            result = []
            for i in range(42):
                dec = ror(data[i], ror_pattern[i]) ^ xor_pattern[i]
                result.append(dec)
            
            try:
                text = bytes(result).decode('ascii')
                if text.startswith('uoftctf{') and text.endswith('}'):
                    print(f"\n*** FOUND with {pattern_name} ROR + {xor_pattern_name} XOR ***")
                    print(text)
            except:
                pass
