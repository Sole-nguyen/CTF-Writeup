# -*- coding: utf-8 -*-
"""
Automated extractor using radare2 to analyze all f_X functions
"""

import subprocess
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

# Based on manual analysis of f_0, f_11, f_12:
decrypt_ops = {
    4: ('sub', 0x0A),   # f_0: add 0x0A -> decrypt: sub 0x0A
    38: ('sub', 0x70),  # f_11: add 0x70 -> decrypt: sub 0x70
    39: ('xor', 0xA7),  # f_12: xor 0xFFFFFFA7 -> decrypt: xor 0xA7
}

print("Extracting all functions using radare2...")
print("This will analyze checker_unpacked and extract operations\n")

try:
    # Use radare2 to disassemble all f_X functions
    for func_num in range(75):
        func_name = f"sym.f_{func_num}"
        
        # Get disassembly of the function
        cmd = f'r2 -qc "aaa; pdf @ {func_name}" checker_unpacked'
        result = subprocess.run(
            ['wsl', 'bash', '-c', cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0 or not result.stdout:
            continue
        
        disasm = result.stdout
        
        # Parse the disassembly to find:
        # 1. Position: look for "add rax, 0xXX"
        # 2. Operation: look for "add/sub/xor edx, 0xXX"
        
        position = None
        operation = None
        op_value = None
        
        for line in disasm.split('\n'):
            # Find position
            m = re.search(r'add\s+rax,\s+0x([0-9a-f]+)', line, re.I)
            if m:
                position = int(m.group(1), 16)
            
            # Find operation on edx
            m = re.search(r'(add|sub|xor)\s+edx,\s+0x([0-9a-f]+)', line, re.I)
            if m:
                operation = m.group(1).lower()
                op_value = int(m.group(2), 16) & 0xFF  # Take only lower byte
        
        if position is not None and operation and op_value is not None:
            # Determine inverse operation for decryption
            if operation == 'add':
                decrypt_ops[position] = ('sub', op_value)
            elif operation == 'sub':
                decrypt_ops[position] = ('add', op_value)
            elif operation == 'xor':
                decrypt_ops[position] = ('xor', op_value)
            
            print(f"f_{func_num}: pos={position}, encrypt={operation} 0x{op_value:02x}, decrypt={decrypt_ops[position][0]} 0x{decrypt_ops[position][1]:02x}")

except Exception as e:
    print(f"Error extracting with radare2: {e}")
    print("\nUsing manual analysis from the 3 functions shown...")

print(f"\n{'='*60}")
print(f"Total operations found: {len(decrypt_ops)}")
print(f"{'='*60}\n")

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

try:
    flag = bytes(result).decode('ascii')
    print(f"Decrypted flag: {flag}")
    
    if flag.startswith('uoftctf{') and flag.endswith('}'):
        print("\n✓✓✓ FLAG FOUND! ✓✓✓")
    else:
        print(f"\nPartial success - need to extract more functions")
        print(f"Positions decoded so far: {sorted(decrypt_ops.keys())}")
except Exception as e:
    print(f"Decode error: {e}")
    print(f"Partial result: {result}")
