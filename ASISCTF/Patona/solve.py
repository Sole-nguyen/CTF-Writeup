#!/usr/bin/env python3

# Read the encrypted flag
with open('flag.raw', 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes")
print(f"First 50 bytes: {data[:50]}")
print(f"Unique bytes: {len(set(data))}")

# Analyze the pattern - looking at the repeating characters
# The data appears to have Arabic characters: ب ج ت ث ش خ etc.
# These seem to be some encoding

# Let's look at character frequency
from collections import Counter
freq = Counter(data)
print(f"\nMost common bytes:")
for byte, count in freq.most_common(20):
    print(f"  {hex(byte)}: {count} times ({chr(byte) if 32 <= byte < 127 else '?'})")

# Looking at the pattern, I can see repeating sequences
# Let me try to find patterns
print(f"\nLooking for 'ASIS' pattern...")

# The challenge name is "Patona" which might give us a clue
# Let's try XOR with different keys
def try_xor_key(data, key):
    result = bytearray()
    key_bytes = key if isinstance(key, bytes) else key.encode()
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

# Try common keys
for key in [b'ASIS', b'patona', b'Patona', b'PATONA', b'flag', b'key']:
    result = try_xor_key(data[:100], key)
    if b'ASIS{' in result or b'asis{' in result:
        print(f"\nFound with key {key}!")
        full_result = try_xor_key(data, key)
        print(full_result[:200])
        break
else:
    # Try single byte XOR
    print("\nTrying single-byte XOR...")
    for key_byte in range(256):
        result = bytes([b ^ key_byte for b in data[:100]])
        if b'ASIS' in result or b'asis' in result or b'flag' in result:
            print(f"\nFound with single byte key {hex(key_byte)} ({key_byte})!")
            full_result = bytes([b ^ key_byte for b in data])
            print(full_result.decode('utf-8', errors='ignore')[:500])
            # Save to file
            with open('decoded.txt', 'wb') as f:
                f.write(full_result)
            break
