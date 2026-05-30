# -*- coding: utf-8 -*-
"""
Find the EXACT transformation chain for position 0
We know: 'u' (0x75) -> 0x65
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

# For each position, try TWO-STEP transformations
print("Trying 2-step transformations for known 'uoftctf{' -> first 8 bytes:\n")

known_plain = list(b"uoftctf{")
ops = {
    'xor': lambda b, n: b ^ n,
    'ror': lambda b, n: ror(b, n),
    'rol': lambda b, n: rol(b, n),
    'add': lambda b, n: (b + n) & 0xFF,
    'sub': lambda b, n: (b - n) & 0xFF,
    'not': lambda b, n: (~b) & 0xFF,
}

solutions = {}

for pos in range(min(8, len(known_plain))):
    plain = known_plain[pos]
    cipher = data[pos]
    
    found = []
    
    # Try 2-step: op1(plain, param1) then op2(result, param2)
    for op1_name, op1_func in ops.items():
        for param1 in range(256) if op1_name != 'not' else [0]:
            if op1_name in ['ror', 'rol'] and param1 >= 8:
                continue
                
            intermediate = op1_func(plain, param1)
            
            for op2_name, op2_func in ops.items():
                for param2 in range(256) if op2_name != 'not' else [0]:
                    if op2_name in ['ror', 'rol'] and param2 >= 8:
                        continue
                    
                    result = op2_func(intermediate, param2)
                    
                    if result == cipher:
                        desc = f"{op1_name}({param1 if op1_name != 'not' else ''}) -> {op2_name}({param2 if op2_name != 'not' else ''})"
                        found.append(desc)
                        if len(found) <= 3:  # Only show first few
                            print(f"Pos {pos} ('{chr(plain)}'): {desc}")
    
    solutions[pos] = found
    if not found:
        print(f"Pos {pos} ('{chr(plain)}'): *** NO 2-STEP SOLUTION FOUND ***")
    print()

# Now try to find a pattern
print("\n" + "="*60)
print("Looking for patterns in the transformations...")
print("="*60)

# Check if same transformation works for all positions
for op1_name in ops.keys():
    for param1_pattern in ['constant', 'position', 'pos*2']:
        for op2_name in ops.keys():
            for param2_pattern in ['constant', 'position', 'pos*2']:
                # Try to apply this pattern to all 42 bytes
                success = True
                result = []
                
                for pos in range(42):
                    # Determine parameters based on pattern
                    if param1_pattern == 'constant':
                        param1 = pos if op1_name in ['ror', 'rol'] else 0x10  # Try 0x10 as constant
                    elif param1_pattern == 'position':
                        param1 = pos
                    else:  # pos*2
                        param1 = (pos * 2) & 0xFF
                    
                    if param2_pattern == 'constant':
                        param2 = 0 if op2_name == 'not' else 0x10
                    elif param2_pattern == 'position':
                        param2 = pos
                    else:  # pos*2
                        param2 = (pos * 2) & 0xFF
                    
                    # Apply inverse transformation
                    cipher = data[pos]
                    
                    # Inverse of op2
                    if op2_name == 'xor':
                        intermediate = cipher ^ param2
                    elif op2_name == 'not':
                        intermediate = (~cipher) & 0xFF
                    elif op2_name == 'ror':
                        intermediate = rol(cipher, param2 % 8)
                    elif op2_name == 'rol':
                        intermediate = ror(cipher, param2 % 8)
                    elif op2_name == 'add':
                        intermediate = (cipher - param2) & 0xFF
                    elif op2_name == 'sub':
                        intermediate = (cipher + param2) & 0xFF
                    else:
                        continue
                    
                    # Inverse of op1
                    if op1_name == 'xor':
                        plain = intermediate ^ param1
                    elif op1_name == 'not':
                        plain = (~intermediate) & 0xFF
                    elif op1_name == 'ror':
                        plain = rol(intermediate, param1 % 8)
                    elif op1_name == 'rol':
                        plain = ror(intermediate, param1 % 8)
                    elif op1_name == 'add':
                        plain = (intermediate - param1) & 0xFF
                    elif op1_name == 'sub':
                        plain = (intermediate + param1) & 0xFF
                    else:
                        continue
                    
                    result.append(plain)
                
                # Check if result looks like a flag
                try:
                    text = bytes(result).decode('ascii')
                    if text.startswith('uoftctf{') and text.endswith('}'):
                        print(f"\n*** FOUND FLAG ***")
                        print(f"Transformation: {op1_name}({param1_pattern}) -> {op2_name}({param2_pattern})")
                        print(f"Flag: {text}")
                        exit(0)
                except:
                    pass

print("\nNo pattern found with 2-step transformations.")
print("The transformation might be more complex or use lookup tables.")
