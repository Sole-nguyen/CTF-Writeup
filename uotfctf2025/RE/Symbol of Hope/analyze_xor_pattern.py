# -*- coding: utf-8 -*-
data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

# We know position 0: 'u' (0x75) ^ 0x10 = 0x65
# Maybe the XOR key increments or follows a pattern

# Assuming flag = "uoftctf{...}", calculate what the XOR key sequence would be
assumed_flag_start = list(b"uoftctf{")

print("XOR key sequence if flag starts with 'uoftctf{':")
xor_keys = []
for i in range(len(assumed_flag_start)):
    xor_key = data[i] ^ assumed_flag_start[i]
    xor_keys.append(xor_key)
    print(f"Position {i}: 0x{xor_key:02x} ({xor_key})")

# Check if the XOR keys follow a mathematical pattern
print(f"\nXOR keys: {[f'0x{k:02x}' for k in xor_keys]}")
print(f"As decimal: {xor_keys}")

# Check differences between consecutive keys
diffs = [xor_keys[i+1] - xor_keys[i] for i in range(len(xor_keys)-1)]
print(f"Differences: {diffs}")

# Maybe the key is: 0x10 + f(position)?
# Try: key[i] = (0x10 + i * multiplier) % 256
for mult in range(1, 50):
    keys_formula = [(0x10 + i * mult) % 256 for i in range(42)]
    if keys_formula[:8] == xor_keys:
        print(f"\n*** Pattern found: key[i] = (0x10 + {mult}*i) % 256 ***")
        # Decode full message
        result = bytes([data[i] ^ keys_formula[i] for i in range(42)])
        try:
            text = result.decode('ascii')
            print(f"Flag: {text}")
            exit(0)
        except:
            print(f"Decode failed: {result}")
        break

# Try Fibonacci-like or other sequences
print("\nTrying other patterns...")

# Maybe it's: key = f(i) where f is some hash or transformation
# Let's try key[i] = (i * i) % 256
keys_formula = [(i * i) % 256 for i in range(42)]
result = bytes([data[i] ^ keys_formula[i] for i in range(42)])
try:
    text = result.decode('ascii')
    if text.startswith('uoftctf{'):
        print(f"*** Found with i^2: {text} ***")
except:
    pass

# Try key[i] = (i * 0x10) % 256
keys_formula = [(i * 0x10) % 256 for i in range(42)]
result = bytes([data[i] ^ keys_formula[i] for i in range(42)])
try:
    text = result.decode('ascii')
    if text.startswith('uoftctf{'):
        print(f"*** Found with i*0x10: {text} ***")
except:
    pass

print("\nNo simple pattern found in XOR keys.")
