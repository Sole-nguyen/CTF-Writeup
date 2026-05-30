#!/usr/bin/env python3
"""
Fresh approach to solve Patona challenge
"""

import re
from collections import Counter

# Read the encrypted file
with open('flag.raw', 'rb') as f:
    data = f.read()

# Decode as UTF-8
text = data.decode('utf-8', errors='replace')

print(f"File size: {len(data)} bytes")
print(f"Text length: {len(text)} characters")
print(f"Unique chars: {len(set(text))}")

# Frequency analysis
freq = Counter(text)
sorted_chars = [ch for ch, _ in freq.most_common()]

print("\nTop 30 characters by frequency:")
for i, ch in enumerate(sorted_chars[:30]):
    print(f"{i:2d}. U+{ord(ch):04X} '{ch}' : {freq[ch]:6d}")

# Strategy 1: Simple character substitution based on frequency
# English letter frequency: ETAOIN SHRDLU
# In flags/code: space, underscore, common letters

# Common characters in CTF flags with ASIS{...} format
target_freq = ' etaoinsrhldcumfpgwybvkxjqz_ETAOINSRHLDCUMFPGWYBVKXJQZ0123456789{}[]():-.,;!?'

mapping = {}
for i, ch in enumerate(sorted_chars):
    if i < len(target_freq):
        mapping[ch] = target_freq[i]
    else:
        mapping[ch] = '?'

decoded1 = ''.join(mapping.get(ch, ch) for ch in text)

print("\n" + "="*80)
print("ATTEMPT 1: Frequency-based substitution")
print("="*80)
print(decoded1[:500])

# Look for ASIS{ pattern
flags1 = re.findall(r'ASIS\{[^}]+\}', decoded1, re.IGNORECASE)
if flags1:
    print(f"\n*** FOUND FLAG: {flags1[0]} ***")
else:
    print("\nNo flag found in attempt 1")

# Strategy 2: Try mapping with priority for flag structure
# Put ASIS{} characters first
flag_priority = 'ASIS{} _etaoinsrhldcumfpgwybvkxjqz0123456789-'
mapping2 = {}
for i, ch in enumerate(sorted_chars):
    if i < len(flag_priority):
        mapping2[ch] = flag_priority[i]
    else:
        mapping2[ch] = chr(ord('a') + (i - len(flag_priority)) % 26)

decoded2 = ''.join(mapping2.get(ch, ch) for ch in text)

print("\n" + "="*80)
print("ATTEMPT 2: Flag-priority substitution")
print("="*80)
print(decoded2[:500])

flags2 = re.findall(r'ASIS\{[^}]+\}', decoded2, re.IGNORECASE)
if flags2:
    print(f"\n*** FOUND FLAG: {flags2[0]} ***")
else:
    print("\nNo flag found in attempt 2")

# Strategy 3: XOR bruteforce
print("\n" + "="*80)
print("ATTEMPT 3: XOR bruteforce")
print("="*80)

# Single byte XOR
for key in range(256):
    xored = bytes([b ^ key for b in data])
    try:
        decoded3 = xored.decode('utf-8', errors='ignore')
        if 'ASIS{' in decoded3:
            print(f"\n*** FOUND with XOR key {key} (0x{key:02x}) ***")
            print(decoded3[:500])
            flags3 = re.findall(r'ASIS\{[^}]+\}', decoded3)
            if flags3:
                print(f"\n*** FLAG: {flags3[0]} ***")
                break
    except:
        pass

# Multi-byte XOR with common keys
common_keys = [
    b'ASIS', b'patona', b'Patona', b'PATONA', 
    b'flag', b'FLAG', b'key', b'KEY', b'ctf', b'CTF',
    b'password', b'secret', b'crypto'
]

for key in common_keys:
    xored = bytearray()
    for i, byte in enumerate(data):
        xored.append(byte ^ key[i % len(key)])
    
    try:
        decoded_xor = bytes(xored).decode('utf-8', errors='ignore')
        if 'ASIS{' in decoded_xor:
            print(f"\n*** FOUND with multi-byte XOR key {key} ***")
            print(decoded_xor[:500])
            flags = re.findall(r'ASIS\{[^}]+\}', decoded_xor)
            if flags:
                print(f"\n*** FLAG: {flags[0]} ***")
                break
    except:
        pass

# Strategy 4: Look at the actual character pattern more carefully
print("\n" + "="*80)
print("ATTEMPT 4: Pattern analysis")
print("="*80)

# Show first 100 chars and their Unicode points
print("First 100 characters with codes:")
for i in range(min(100, len(text))):
    ch = text[i]
    print(f"{ch} (U+{ord(ch):04X})", end=' ')
    if (i+1) % 10 == 0:
        print()

print("\n\nSaving full decoded outputs for manual review...")
with open('decoded1_freq.txt', 'w', encoding='utf-8') as f:
    f.write(decoded1)

with open('decoded2_flagpri.txt', 'w', encoding='utf-8') as f:
    f.write(decoded2)

print("\nFiles saved: decoded1_freq.txt, decoded2_flagpri.txt")
print("\nCheck these files for flag patterns!")
