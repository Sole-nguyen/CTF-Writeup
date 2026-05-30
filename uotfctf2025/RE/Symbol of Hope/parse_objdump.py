# -*- coding: utf-8 -*-
"""
Parse objdump output to extract all f_X function operations
"""
import re

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

decrypt_ops = {}

print("Parsing all_functions.txt...")

try:
    with open('all_functions.txt', 'r') as f:
        lines = f.readlines()
    
    func_num = None
    position = None
    operation = None
    op_value = None
    
    for line in lines:
        # Detect new function
        m = re.search(r'<f_(\d+)>', line)
        if m:
            # Save previous function if any
            if func_num is not None and position is not None and operation and op_value is not None:
                # Determine inverse operation
                if operation == 'add':
                    inv_op = ('sub', op_value)
                elif operation == 'sub':
                    inv_op = ('add', op_value)
                elif operation == 'xor':
                    inv_op = ('xor', op_value)
                elif operation == 'imul':
                    inv_op = ('imul_inv', op_value)
                else:
                    inv_op = None
                
                if inv_op:
                    decrypt_ops[position] = inv_op
                    print(f"f_{func_num:2d}: pos={position:2d} ({position:02X}h), encrypt={operation} 0x{op_value:02X}")
            
            # Start new function
            func_num = int(m.group(1))
            position = None
            operation = None
            op_value = None
            continue
        
        if func_num is None:
            continue
        if func_num is None:
            continue
        
        # Find position: add $0xXX,%rax
        m = re.search(r'add\s+\$0x([0-9a-f]+),%rax', line)
        if m:
            position = int(m.group(1), 16)
        
        # Find operations on registers
        # Pattern 1: mov $0xXX,%ecx (value for imul)
        m = re.search(r'mov\s+\$0x([0-9a-f]+),%ecx', line)
        if m:
            temp_val = int(m.group(1), 16)
            # Convert to signed if needed
            if temp_val > 0x7FFFFFFF:
                temp_val = -(0x100000000 - temp_val)
            op_value = temp_val & 0xFF
        
        # Pattern 2: direct add/sub/xor with value
        m = re.search(r'(add|sub|xor)\s+\$0x([0-9a-f]+),', line)
        if m:
            operation = m.group(1)
            op_value = int(m.group(2), 16) & 0xFF
        
        # Pattern 3: imul (multiply)
        if 'imul' in line and op_value is not None:
            operation = 'imul'
    
    # Don't forget last function
    if func_num is not None and position is not None and operation and op_value is not None:
        if operation == 'add':
            inv_op = ('sub', op_value)
        elif operation == 'sub':
            inv_op = ('add', op_value)
        elif operation == 'xor':
            inv_op = ('xor', op_value)
        elif operation == 'imul':
            inv_op = ('imul_inv', op_value)
        else:
            inv_op = None
        
        if inv_op:
            decrypt_ops[position] = inv_op
            print(f"f_{func_num:2d}: pos={position:2d} ({position:02X}h), encrypt={operation} 0x{op_value:02X}")

except FileNotFoundError:
    print("all_functions.txt not found!")
    exit(1)

print(f"\n{'='*60}")
print(f"Total operations found: {len(decrypt_ops)}")
print(f"{'='*60}\n")

# Special handling for imul - need modular inverse
def mod_inverse(a, m=256):
    """Find modular multiplicative inverse of a mod m"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

# Apply decryption
result = list(data)
for pos in sorted(decrypt_ops.keys()):
    op, val = decrypt_ops[pos]
    
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
    elif op == 'imul_inv':
        # Multiply then take modular inverse
        inv = mod_inverse(val)
        if inv:
            result[pos] = (result[pos] * inv) & 0xFF
        else:
            print(f"WARNING: Cannot find inverse of {val} for position {pos}")

try:
    flag = bytes(result).decode('ascii')
    print(f"\nDecrypted flag: {flag}")
    
    if flag.startswith('uoftctf{') and flag.endswith('}'):
        print("\n" + "="*60)
        print("✓✓✓ FLAG FOUND! ✓✓✓")
        print("="*60)
    else:
        print(f"\nPartial success. Positions decoded: {sorted(decrypt_ops.keys())}")
except Exception as e:
    print(f"Decode error: {e}")
    # Show first 20 bytes
    print(f"First 20 bytes: {result[:20]}")
    print(f"As chars: {[chr(b) if 32<=b<127 else '?' for b in result[:20]]}")
