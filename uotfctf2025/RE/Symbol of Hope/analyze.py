# -*- coding: utf-8 -*-
data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

print(f"Length: {len(data)}")
print(f"Data: {' '.join(f'{b:02x}' for b in data)}")
print()

# Try subtracting each byte by its position
print("=== Subtract by position ===")
result = []
for i, b in enumerate(data):
    result.append(b - i)
result_str = ''.join([chr(b % 256) if 32 <= (b % 256) < 127 else '?' for b in result])
print(f"Result: {result_str}")
print(f"Hex: {' '.join(f'{(b % 256):02x}' for b in result)}")

# Try adding each byte by its position
print("\n=== Add by position ===")
result = []
for i, b in enumerate(data):
    result.append((b + i) % 256)
result_str = ''.join([chr(b) if 32 <= b < 127 else '?' for b in result])
print(f"Result: {result_str}")
print(f"Hex: {' '.join(f'{b:02x}' for b in result)}")

# Try XOR with position
print("\n=== XOR with position ===")
result = []
for i, b in enumerate(data):
    result.append(b ^ i)
result_str = ''.join([chr(b) if 32 <= b < 127 else '?' for b in result])
print(f"Result: {result_str}")
print(f"Hex: {' '.join(f'{b:02x}' for b in result)}")

# Try looking for flag format patterns
# uoftctf{ = 75 6f 66 74 63 74 66 7b
print("\n=== Check if XOR reveals 'uoftctf{' ===")
target = [0x75, 0x6f, 0x66, 0x74, 0x63, 0x74, 0x66, 0x7b]
for i in range(len(data) - len(target) + 1):
    key = []
    for j in range(len(target)):
        key.append(data[i+j] ^ target[j])
    # Check if the key is consistent or follows a pattern
    if len(set(key)) == 1:  # All same byte
        print(f"Position {i}: Single byte key = 0x{key[0]:02x}")
        full_result = ''.join([chr(b ^ key[0]) for b in data])
        print(f"  Full result: {full_result}")
    elif len(set(key)) <= 3:  # Small number of different bytes
        print(f"Position {i}: Key pattern = {' '.join(f'{k:02x}' for k in key)}")

# Try repeating key XOR
print("\n=== Try repeating key XOR (lengths 2-10) ===")
for key_len in range(2, 11):
    for offset in range(len(data) - key_len + 1):
        # Try to derive key from first key_len bytes
        test_plaintext = b"uoftctf{"[:key_len]
        key = bytes([data[offset + i] ^ test_plaintext[i] for i in range(min(key_len, len(test_plaintext)))])
        
        # Apply the key to all data
        result = []
        for i, b in enumerate(data):
            result.append(b ^ key[i % len(key)])
        
        result_str = bytes(result)
        try:
            result_text = result_str.decode('ascii')
            if 'uoftctf{' in result_text:
                print(f"Key length {key_len}, offset {offset}: key={key.hex()}")
                print(f"  Result: {result_text}")
        except:
            pass
