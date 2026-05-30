import re

# Simple pattern matching
functions = {}

with open('objdump_output.txt', 'r') as f:
    content = f.read()

# Split by functions
func_blocks = re.findall(r'<f_(\d+)>:?\s*(.*?)(?=<f_\d+>:|$)', content, re.DOTALL)

print(f"Found {len(func_blocks)} functions\n")

for func_num_str, block in func_blocks:
    func_num = int(func_num_str)
    
    # Find position: add rax,0xXX (Intel syntax)
    pos_match = re.search(r'add\s+rax,0x([0-9a-f]+)', block)
    if not pos_match:
        continue
    position = int(pos_match.group(1), 16)
    
    # Check for XOR operation: xor eax,0xXX
    xor_match = re.search(r'xor\s+eax,0x([0-9a-f]+)', block)
    if xor_match:
        value = int(xor_match.group(1), 16)
        functions[func_num] = (position, 'xor', value)
        print(f"f_{func_num:2d}: pos={position:2d}, XOR 0x{value:02X}")
        continue
    
    # Check for IMUL operation: imul eax,ecx
    imul_match = re.search(r'imul\s+eax,ecx', block)
    if imul_match:
        # Get the value from mov ecx,0xXX
        mov_match = re.search(r'mov\s+ecx,0x([0-9a-f]+)', block)
        if mov_match:
            value = int(mov_match.group(1), 16)
            # Convert to signed if needed
            if value > 0x7FFFFFFF:
                value = -(0x100000000 - value)
            value = value & 0xFF  # Only keep byte
            functions[func_num] = (position, 'imul', value)
            print(f"f_{func_num:2d}: pos={position:2d}, IMUL 0x{value:02X}")
            continue
    
    # Check for ADD operation: add eax,0xXX
    add_match = re.search(r'add\s+eax,0x([0-9a-f]+)', block)
    if add_match:
        value = int(add_match.group(1), 16)
        functions[func_num] = (position, 'add', value)
        print(f"f_{func_num:2d}: pos={position:2d}, ADD 0x{value:02X}")
        continue
    
    # Check for SUB operation: sub eax,0xXX
    sub_match = re.search(r'sub\s+eax,0x([0-9a-f]+)', block)
    if sub_match:
        value = int(sub_match.group(1), 16)
        functions[func_num] = (position, 'sub', value)
        print(f"f_{func_num:2d}: pos={position:2d}, SUB 0x{value:02X}")
        continue

print(f"\n\nTotal operations extracted: {len(functions)}")

# Now decrypt
with open('checker_unpacked', 'rb') as f:
    f.seek(0x41020)
    encrypted = list(f.read(42))

print(f"\nEncrypted data: {' '.join(f'{b:02X}' for b in encrypted)}")

# Build position -> operation mapping
decrypt_ops = {}
for func_num, (position, operation, value) in functions.items():
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
        decrypt_ops[position] = ('imul', inv)

# Apply decryption
decrypted = encrypted[:]
for pos in sorted(decrypt_ops.keys()):
    op, val = decrypt_ops[pos]
    if op == 'xor':
        decrypted[pos] = (decrypted[pos] ^ val) & 0xFF
    elif op == 'add':
        decrypted[pos] = (decrypted[pos] + val) & 0xFF
    elif op == 'sub':
        decrypted[pos] = (decrypted[pos] - val) & 0xFF
    elif op == 'imul':
        decrypted[pos] = (decrypted[pos] * val) & 0xFF

try:
    flag = bytes(decrypted).decode('ascii')
    print(f"\nDecrypted flag: {flag}")
except:
    print(f"\nDecrypted bytes: {decrypted}")
    print(f"As chars: {[chr(b) if 32 <= b < 127 else '?' for b in decrypted]}")
