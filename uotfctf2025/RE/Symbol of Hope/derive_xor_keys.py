# -*- coding: utf-8 -*-
"""
It looks like each byte is XOR'd with a different key!
Let's derive the full XOR key from "uoftctf{" and try to decode
"""

data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

# Known prefix
known_prefix = b"uoftctf{"
known_suffix = b"}"

# Derive XOR keys from known prefix
xor_keys = []
for i in range(len(known_prefix)):
    xor_keys.append(data[i] ^ known_prefix[i])

# Derive XOR key from known suffix
xor_keys_end = [data[-1] ^ ord('}')]

print("XOR keys derived from 'uoftctf{':")
print(f"  {[f'0x{k:02x}' for k in xor_keys]}")
print(f"  Decimal: {xor_keys}")

print(f"\nXOR key for last byte (assuming '}}'):")
print(f"  0x{xor_keys_end[0]:02x} ({xor_keys_end[0]})")

# Check if there's a pattern that can help us derive the middle keys
# Try common patterns:

patterns_to_try = [
    # Maybe it's based on a hash or PRNG seeded with something
    # Or maybe it cycles with a longer period
    
    # Try assuming the key repeats every 8 bytes
    lambda i: xor_keys[i % len(xor_keys)],
    
    # Try linear extrapolation
    lambda i: (xor_keys[0] + i * 13) & 0xFF,
    
    # Try XOR with the character's ASCII value AND position
    lambda i: xor_keys[0] ^ i,
]

print("\nTrying to extrapolate the XOR key pattern...")

for pattern_idx, pattern_func in enumerate(patterns_to_try):
    full_keys = [pattern_func(i) for i in range(42)]
    
    result = bytes([data[i] ^ full_keys[i] for i in range(42)])
    
    try:
        text = result.decode('ascii')
        if text.startswith('uoftctf{') and text.endswith('}'):
            print(f"\n*** FOUND FLAG with pattern {pattern_idx} ***")
            print(text)
            exit(0)
        elif all(32 <= b < 127 for b in result[:20]):
            print(f"Pattern {pattern_idx}: {text[:20]}...")
    except:
        pass

# If patterns don't work, we need to look at the binary to find the key generation
print("\n" + "="*60)
print("Could not find the XOR key pattern automatically.")
print("Please check in IDA for:")
print("1. An array/buffer containing XOR keys")
print("2. A function that generates keys (maybe seeded with a constant)")
print("3. The keys might be: [16, 217, 239, 20, 161, 71, 98, 128, ...]")
print("="*60)

# Let me try to find if there's a mathematical relationship
print("\nAnalyzing XOR key relationships:")
for i in range(len(xor_keys) - 1):
    diff = xor_keys[i+1] - xor_keys[i]
    xor_diff = xor_keys[i+1] ^ xor_keys[i]
    print(f"  key[{i}]->key[{i+1}]: diff={diff:4d}, XOR=0x{xor_diff:02x}")
