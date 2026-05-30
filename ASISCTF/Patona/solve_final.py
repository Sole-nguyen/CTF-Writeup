#!/usr/bin/env python3

# Just do the basics - read and decode
with open('flag.raw', 'rb') as f:
    data = f.read()

# Sample the first bytes
sample = data[:100]
print("First 100 bytes in hex:")
print(sample.hex())
print()

# Try decoding
text = data.decode('utf-8', errors='replace')

# Get unique characters and their counts
from collections import Counter
freq = Counter(text)

# List all unique characters sorted by frequency
chars_by_freq = [(ch, cnt) for ch, cnt in freq.most_common()]

print(f"File has {len(chars_by_freq)} unique characters\n")
print("Characters ranked by frequency:")
print("Rank | Char | Unicode | Count")
print("-" * 40)
for i, (ch, cnt) in enumerate(chars_by_freq):
    # Show character, its unicode, and count
    display = ch if ch.isprintable() else '�'
    print(f"{i:4d} | {display:4s} | U+{ord(ch):04X} | {cnt:6d}")

# Now let's build a simple frequency-based substitution
# Most common English: " etaoinsrhldcumfpgwybvkjxqz"
target = " etaoinsrhldcumfpgwybvkjxqzETAOINSRHLDCUMFPGWYBVKJXQZ0123456789_-.,;:!?()[]{}\"'/@#$%&*+=<>\\|`~"

substitution = {}
for i, (ch, _) in enumerate(chars_by_freq):
    if i < len(target):
        substitution[ch] = target[i]
    else:
        substitution[ch] = '?'

# Apply substitution
result = ''.join(substitution.get(c, c) for c in text)

print("\n" + "="*80)
print("SUBSTITUTION DECODE (first 2000 chars):")
print("="*80)
print(result[:2000])

# Search for flag pattern
import re
flags = re.findall(r'ASIS\{[^}]{10,100}\}', result, re.IGNORECASE | re.DOTALL)

if flags:
    print("\n" + "*"*80)
    print("POTENTIAL FLAGS FOUND:")
    for flag in flags:
        print(f"  {flag}")
    print("*"*80)
    
    # Save the first one
    with open('SOLUTION.txt', 'w') as f:
        f.write(f"FLAG: {flags[0]}\n")
    print("\nSaved to SOLUTION.txt")
else:
    print("\n[No ASIS{...} pattern found yet]")
    
# Save full result for manual inspection
with open('substitution_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)
print("Full result saved to substitution_result.txt")
