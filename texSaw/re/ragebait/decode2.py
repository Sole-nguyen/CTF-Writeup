#!/usr/bin/env python3
import subprocess

binary_path = './ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY'

# Get all strings from the binary
result = subprocess.run(['strings', binary_path], capture_output=True, text=True)
strings_list = result.stdout.split('\n')

# Filter strings that end with 'H'
encoded_strings = [s for s in strings_list if s.endswith('H') and len(s) > 5]

print(f"Found {len(encoded_strings)} encoded strings ending with 'H'\n")

# XOR key is 86 (0x56) based on the patterns we saw
XOR_KEY = 86

print("Decoding all strings with XOR key 86:")
print("=" * 60)

decoded_flags = []
for s in encoded_strings:
    # Remove the 'H' marker and decode
    encoded = s[:-1]
    decoded = ''.join(chr(ord(c) ^ XOR_KEY) for c in encoded)
    
    # Check if it looks like a real flag or message
    if 'texsaw{' in decoded:
        print(f"*** FLAG FOUND: {decoded}")
        decoded_flags.append(decoded)
    elif all(32 <= ord(c) < 127 for c in decoded):
        print(f"{decoded}")

print("\n" + "=" * 60)
print(f"\nTotal decoded flags: {len(decoded_flags)}")
for flag in decoded_flags:
    print(f"  {flag}")
