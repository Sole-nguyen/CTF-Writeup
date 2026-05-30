#!/usr/bin/env python3
import sys

with open('flag.raw', 'rb') as f:
    data = f.read()

# First, let's see the raw bytes
print(f"File size: {len(data)} bytes")
print(f"\nFirst 50 bytes (hex): {data[:50].hex()}")
print(f"\nFirst 50 bytes (dec): {list(data[:50])}")

# Try to decode as UTF-8 and see what we get
text = data.decode('utf-8', errors='replace')
print(f"\nFirst 100 characters (UTF-8): {repr(text[:100])}")

# Character frequency
from collections import Counter
freq = Counter(text)
print(f"\nUnique characters: {len(freq)}")
print(f"\nTop 20 chars:")
for i, (ch, cnt) in enumerate(freq.most_common(20)):
    print(f"{i:2d}. '{ch}' U+{ord(ch):04X} : {cnt}")

# Now let's try the key insight: this might be a simple substitution
# Map the most frequent char to space, next to 'e', etc.
sorted_by_freq = [ch for ch, _ in freq.most_common()]

# English frequency for comparison
english_freq = ' etaoinshrdlcumwfgypbvkjxqz_-,.;:!?0123456789ETAOINSHR DLCUMWFGYPBVKJXQZ{}[]()"\'/'

# Build mapping
mapping = {}
for i, ch in enumerate(sorted_by_freq):
    if i < len(english_freq):
        mapping[ch] = english_freq[i]
    else:
        mapping[ch] = '?'

decoded = ''.join(mapping.get(ch, ch) for ch in text)

print(f"\n\n{'='*70}")
print("DECODED TEXT (first 1000 chars):")
print('='*70)
print(decoded[:1000])

# Look for ASIS{ pattern
import re
matches = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
if matches:
    print(f"\n\n{'*'*70}")
    print(f"FOUND FLAG: {matches[0]}")
    print('*'*70)
    with open('FLAG.txt', 'w') as f:
        f.write(matches[0])
else:
    print("\n\nNo ASIS{} pattern found. Let's try other mappings...")
    
    # Try with flag chars prioritized
    flag_chars = 'ASIS{}_'
    extended = ' etaoinsrhldcumwfgypbvkxjqz0123456789-.,;:!?ETAOINSRHLDCUMWFGYPBVKXJQZ[]()"\'/\\'
    
    mapping2 = {}
    for i, ch in enumerate(sorted_by_freq):
        if i < len(flag_chars):
            mapping2[ch] = flag_chars[i]
        elif i - len(flag_chars) < len(extended):
            mapping2[ch] = extended[i - len(flag_chars)]
        else:
            mapping2[ch] = '?'
    
    decoded2 = ''.join(mapping2.get(ch, ch) for ch in text)
    print(f"\n\n{'='*70}")
    print("DECODED TEXT V2 (first 1000 chars):")
    print('='*70)
    print(decoded2[:1000])
    
    matches2 = re.findall(r'ASIS\{[^}]+\}', decoded2, re.IGNORECASE)
    if matches2:
        print(f"\n\n{'*'*70}")
        print(f"FOUND FLAG: {matches2[0]}")
        print('*'*70)
        with open('FLAG.txt', 'w') as f:
            f.write(matches2[0])

# Save full decoded text
with open('decoded_full.txt', 'w', encoding='utf-8') as f:
    f.write(decoded)
    
print("\n\nFull decoded text saved to decoded_full.txt")
