# -*- coding: utf-8 -*-
data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

# Known: flag format is uoftctf{...}
plaintext = list(b"uoftctf{")
ciphertext = data[:8]

print("Analyzing transformation from 'uoftctf{' to first 8 bytes:")
print(f"Plaintext:  {' '.join(f'{c:02x}' for c in plaintext)}")
print(f"Ciphertext: {' '.join(f'{c:02x}' for c in ciphertext)}")
print()

for i in range(8):
    p = plaintext[i]
    c = ciphertext[i]
    print(f"Position {i}: '{chr(p)}' (0x{p:02x}) -> 0x{c:02x}")
    print(f"  XOR:     0x{p^c:02x}")
    print(f"  Add:     {(c-p) % 256}")
    print(f"  Sub:     {(p-c) % 256}")
    print()

# Check if there's a pattern in the XOR values
xor_values = [plaintext[i] ^ ciphertext[i] for i in range(8)]
print(f"XOR values: {' '.join(f'0x{v:02x}' for v in xor_values)}")
print(f"XOR as ASCII: {bytes(xor_values)}")

# Check if it's a repeating XOR
print("\nChecking for repeating patterns:")
for key_len in [1, 2, 3, 4]:
    matches = True
    for i in range(key_len, 8):
        if xor_values[i] != xor_values[i % key_len]:
            matches = False
            break
    if matches:
        key = xor_values[:key_len]
        print(f"  Repeating key of length {key_len}: {' '.join(f'0x{k:02x}' for k in key)}")
        # Try to decrypt the whole message with this key
        result = []
        for i, b in enumerate(data):
            result.append(b ^ key[i % len(key)])
        try:
            text = bytes(result).decode('ascii')
            print(f"    Full decryption: {text}")
            if text.startswith('uoftctf{'):
                print(f"    *** THIS IS THE FLAG! ***")
        except:
            print(f"    Full decryption not ASCII")

# Also check the last byte (should be '}' = 0x7d)
closing_brace = ord('}')
print(f"\nLast byte: 0x{data[-1]:02x}")
print(f"If it's '}}' (0x7d), XOR would be: 0x{data[-1] ^ closing_brace:02x}")
