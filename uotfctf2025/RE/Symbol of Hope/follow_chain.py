import re

# Parse all functions and their call targets
functions = {}

with open('objdump_output.txt', 'r') as f:
    content = f.read()

# Split by functions - match f_X functions and capture until the next f_X
func_blocks = re.findall(r'<f_(\d+)>:(.*?)(?=\n[0-9a-f]+ <f_\d+>:|$)', content, re.DOTALL)

print(f"Found {len(func_blocks)} f_X functions\n")

for func_num_str, block in func_blocks:
    func_num = int(func_num_str)
    
    # Find position: add rax,0xXX (or default to 0 if not found)
    pos_match = re.search(r'add\s+rax,0x([0-9a-f]+)', block)
    position = int(pos_match.group(1), 16) if pos_match else 0
    
    # Find which function this calls
    call_match = re.search(r'call[q]?\s+[0-9a-f]+ <f_(\d+)>', block)
    next_func = int(call_match.group(1)) if call_match else None
    
    # Determine operation
    xor_match = re.search(r'xor\s+e[a-z]{2},0x([0-9a-f]+)', block)
    if xor_match:
        value = int(xor_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'xor',
            'value': value,
            'next': next_func
        }
        continue
    
    imul_match = re.search(r'imul\s+eax,ecx', block)
    if imul_match:
        mov_match = re.search(r'mov\s+ecx,0x([0-9a-f]+)', block)
        if mov_match:
            value = int(mov_match.group(1), 16)
            if value > 0x7FFFFFFF:
                value = -(0x100000000 - value)
            value = value & 0xFF
            functions[func_num] = {
                'position': position,
                'operation': 'imul',
                'value': value,
                'next': next_func
            }
            continue
    
    add_match = re.search(r'add\s+e[a-z]{2},0x([0-9a-f]+)', block)
    if add_match:
        value = int(add_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'add',
            'value': value,
            'next': next_func
        }
        continue
    
    sub_match = re.search(r'sub\s+e[a-z]{2},0x([0-9a-f]+)', block)
    if sub_match:
        value = int(sub_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'sub',
            'value': value,
            'next': next_func
        }
        continue
    
    # Check for LEA operation: lea edx,[rax-0xXX] or lea edx,[rax+0xXX]
    lea_sub_match = re.search(r'lea\s+e[a-z]{2},\[.*-0x([0-9a-f]+)\]', block)
    if lea_sub_match:
        value = int(lea_sub_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'sub',
            'value': value,
            'next': next_func
        }
        continue
    
    lea_add_match = re.search(r'lea\s+e[a-z]{2},\[.*\+0x([0-9a-f]+)\]', block)
    if lea_add_match:
        value = int(lea_add_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'add',
            'value': value,
            'next': next_func
        }
        continue
    
    # Check for ROL/ROR: call to rol8/ror8 with mov esi,0xXX before it
    rol_match = re.search(r'mov\s+esi,0x([0-9a-f]+).*?call.*<rol8>', block, re.DOTALL)
    if rol_match:
        value = int(rol_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'rol',
            'value': value,
            'next': next_func
        }
        continue
    
    ror_match = re.search(r'mov\s+esi,0x([0-9a-f]+).*?call.*<ror8>', block, re.DOTALL)
    if ror_match:
        value = int(ror_match.group(1), 16) & 0xFF
        functions[func_num] = {
            'position': position,
            'operation': 'ror',
            'value': value,
            'next': next_func
        }
        continue

print(f"Total operations extracted: {len(functions)}\n")

# Follow the chain starting from f_10 (not f_0 - main calls f_10)
chain = []
current = 10
visited = set()

while current is not None and current not in visited and current in functions:
    visited.add(current)
    func_info = functions[current]
    chain.append((current, func_info))
    print(f"f_{current:2d}: pos={func_info['position']:2d}, {func_info['operation'].upper():4s} 0x{func_info['value']:02X} -> f_{func_info['next'] if func_info['next'] is not None else 'END'}")
    current = func_info['next']

print(f"\n\nChain length: {len(chain)}")
print(f"Expected: 42 bytes to decrypt")

# Build position -> operation mapping from chain
decrypt_ops = {}
for func_num, info in chain:
    position = info['position']
    operation = info['operation']
    value = info['value']
    
    if operation == 'xor':
        decrypt_ops[position] = ('xor', value)
    elif operation == 'add':
        decrypt_ops[position] = ('sub', value)
    elif operation == 'sub':
        decrypt_ops[position] = ('add', value)
    elif operation == 'imul':
        # Need modular inverse
        def modinv(a, m=256):
            a = a % m
            for x in range(1, m):
                if (a * x) % m == 1:
                    return x
            return None
        inv = modinv(value)
        if inv is None:
            print(f"Warning: No modular inverse for {value} (position {position})")
            decrypt_ops[position] = ('imul', value)  # Keep it anyway
        else:
            decrypt_ops[position] = ('imul', inv)

# Apply decryption
with open('checker_unpacked', 'rb') as f:
    f.seek(0x41020)
    encrypted = list(f.read(42))

print(f"\nEncrypted data ({len(encrypted)} bytes):")
print(' '.join(f'{b:02X}' for b in encrypted))

decrypted = encrypted[:]
for pos in sorted(decrypt_ops.keys()):
    if pos >= len(decrypted):
        print(f"Warning: Position {pos} out of range")
        continue
    op, val = decrypt_ops[pos]
    old_val = decrypted[pos]
    if op == 'xor':
        decrypted[pos] = (decrypted[pos] ^ val) & 0xFF
    elif op == 'add':
        decrypted[pos] = (decrypted[pos] + val) & 0xFF
    elif op == 'sub':
        decrypted[pos] = (decrypted[pos] - val) & 0xFF
    elif op == 'imul':
        decrypted[pos] = (decrypted[pos] * val) & 0xFF
    print(f"pos {pos:2d}: {old_val:02X} {op:4s} {val:02X} -> {decrypted[pos]:02X}")

print(f"\n\nDecrypted bytes:")
print(' '.join(f'{b:02X}' for b in decrypted))

try:
    flag = bytes(decrypted).decode('ascii')
    print(f"\n🎉 FLAG: {flag}")
except Exception as e:
    print(f"\nDecode error: {e}")
    printable = ''.join(chr(b) if 32 <= b < 127 else '?' for b in decrypted)
    print(f"As printable: {printable}")
