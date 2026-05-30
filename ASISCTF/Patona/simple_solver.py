#!/usr/bin/env python3
import re
from collections import Counter

# Read flag.raw
with open('flag.raw', 'rb') as f:
    data = f.read()

# Decode as UTF-8
text = data.decode('utf-8', errors='replace')

# Get frequency
freq = Counter(text)
chars_by_freq = [ch for ch, _ in freq.most_common()]

print(f"File: {len(data)} bytes, {len(text)} chars, {len(freq)} unique\n")

# Show top characters
print("Top 30 characters:")
for i in range(min(30, len(chars_by_freq))):
    ch = chars_by_freq[i]
    print(f"{i}: '{ch}' U+{ord(ch):04X} ({freq[ch]})")

print("\n" + "="*80 + "\n")

# Try multiple substitution strategies

# Strategy A: Standard English frequency
print("STRATEGY A: Standard frequency\n")
target_a = ' etaoinsrhldcumfgypbvkxjqzETAOINSRHLDCUMFGYPBVKXJQZ0123456789_-.,;:!?()[]{}"\'/\\@#$%^&*+=<>|`~'
map_a = {chars_by_freq[i]: target_a[i] if i < len(target_a) else '?' for i in range(len(chars_by_freq))}
result_a = ''.join(map_a.get(c, c) for c in text)
print(result_a[:1000])
flags_a = re.findall(r'ASIS\{[^}]{5,100}\}', result_a, re.IGNORECASE)
if flags_a:
    print(f"\n*** FLAG FOUND: {flags_a[0]} ***\n")
    with open('ANSWER.txt', 'w') as f:
        f.write(flags_a[0])
else:
    print("\nNo flag in strategy A\n")

print("="*80 + "\n")

# Strategy B: Flag chars first
print("STRATEGY B: Flag priority\n")
target_b = 'ASIS{}_ etaoinsrhldcumfgypbvkxjqzETOINRHLDCUMFGYPBVKXJQZ0123456789-.,;:!?()[]"\'/\\@#$%^&*+=<>|`~'
map_b = {chars_by_freq[i]: target_b[i] if i < len(target_b) else '?' for i in range(len(chars_by_freq))}
result_b = ''.join(map_b.get(c, c) for c in text)
print(result_b[:1000])
flags_b = re.findall(r'ASIS\{[^}]{5,100}\}', result_b, re.IGNORECASE)
if flags_b:
    print(f"\n*** FLAG FOUND: {flags_b[0]} ***\n")
    with open('ANSWER.txt', 'w') as f:
        f.write(flags_b[0])
else:
    print("\nNo flag in strategy B\n")

print("="*80 + "\n")

# Strategy C: Try XOR
print("STRATEGY C: XOR bruteforce\n")
found_xor = False
for key in range(256):
    xored = bytes([b ^ key for b in data])
    try:
        dec = xored.decode('utf-8', errors='ignore')
        if 'ASIS{' in dec:
            print(f"XOR key 0x{key:02x} found!")
            print(dec[:1000])
            flags_c = re.findall(r'ASIS\{[^}]{5,100}\}', dec)
            if flags_c:
                print(f"\n*** FLAG FOUND: {flags_c[0]} ***\n")
                with open('ANSWER.txt', 'w') as f:
                    f.write(flags_c[0])
                found_xor = True
                break
    except:
        pass

if not found_xor:
    print("No XOR solution found\n")

# Save all results
with open('result_a.txt', 'w', encoding='utf-8') as f:
    f.write(result_a)
with open('result_b.txt', 'w', encoding='utf-8') as f:
    f.write(result_b)

print("\nAll results saved. Check ANSWER.txt if flag was found.")
print("Otherwise check result_a.txt and result_b.txt manually.")
