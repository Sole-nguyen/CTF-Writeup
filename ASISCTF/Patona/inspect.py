#!/usr/bin/env python3

# Read binary data
with open('flag.raw', 'rb') as f:
    data = f.read()

# Show some stats
print(f"Size: {len(data)} bytes\n")

# First 16 bytes
print("First 16 bytes:")
print("Hex:", ' '.join(f'{b:02x}' for b in data[:16]))
print("Dec:", data[:16])
print()

# Now decode and show characters
text = data.decode('utf-8', errors='replace')
print(f"Decoded length: {len(text)} chars")
print(f"First 50 chars: {repr(text[:50])}\n")

# Character codes
print("First 50 character Unicode codes:")
for i, ch in enumerate(text[:50]):
    print(f"U+{ord(ch):04X}", end=' ')
    if (i + 1) % 10 == 0:
        print()
print("\n")

# Unique characters list
unique = sorted(set(text))
print(f"Total unique characters: {len(unique)}")
print("Unique chars:", ''.join(unique))
print()

# Frequency
from collections import Counter
freq = Counter(text)
print("\nCharacter frequency (all):")
for ch, cnt in freq.most_common():
    print(f"'{ch}' (U+{ord(ch):04X}): {cnt}")
