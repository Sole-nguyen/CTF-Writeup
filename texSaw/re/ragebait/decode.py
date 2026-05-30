#!/usr/bin/env python3
import subprocess

binary_path = './ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY'

# Get all strings from the binary
result = subprocess.run(['strings', binary_path], capture_output=True, text=True)
strings_list = result.stdout.split('\n')

# Filter strings that end with 'H' and look encoded
encoded_strings = [s for s in strings_list if s.endswith('H') and len(s) > 5]

print(f"Found {len(encoded_strings)} potentially encoded strings")
print("\nTrying XOR decoding...")

# Try different XOR keys
for key in range(1, 256):
    for s in encoded_strings[:10]:  # Test first 10
        decoded = ''.join(chr(ord(c) ^ key) for c in s)
        if 'texsaw{' in decoded.lower() or 'flag' in decoded.lower():
            print(f"Key {key:3d} (0x{key:02x}): {s[:30]} -> {decoded}")

# Let's also try the specific patterns we saw
test_strings = [
    "$;?%%?98H",
    "8v238?32H", 
    "7/3$vnv&H",
    "&$94:3;xH",
]

print("\nTrying specific strings:")
for s in test_strings:
    for key in range(1, 256):
        decoded = ''.join(chr(ord(c) ^ key) for c in s[:-1])  # Remove 'H'
        if all(32 <= ord(c) < 127 for c in decoded):
            print(f"  {s} XOR {key:3d}: {decoded}")
