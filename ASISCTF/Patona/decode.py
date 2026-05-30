#!/usr/bin/env python3
# Patona CTF Challenge Decoder

with open('flag.raw', 'rb') as f:
    data = f.read()

# Decode as UTF-8
text = data.decode('utf-8', errors='replace')

print(f"Total characters: {len(text)}")

# The pattern shows these Arabic characters repeatedly
# This looks like a substitution cipher
# Looking at the patterns, I need to map these to ASCII

# Common characters in the file (based on the view output):
# ب ت ث ج خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
# And also: , & 6 D V j 

# Let me look for the structure
# The characters seem to repeat in specific patterns

# Based on frequency analysis approach for substitution cipher
from collections import Counter

freq = Counter(text)
print("\nCharacter frequency:")
for char, count in sorted(freq.items(), key=lambda x: -x[1])[:30]:
    print(f"  '{char}' (U+{ord(char):04X}): {count}")

# The most common characters in English are: E T A O I N S H R
# In flag format ASIS{...}, we'd expect: A S I { }

# Let me try a different approach - looking at the hex values
print("\nAnalyzing hex patterns...")
hex_data = data.hex()
print(f"First 200 hex chars: {hex_data[:200]}")

# The Arabic characters are in UTF-8, which means multi-byte sequences
# Let me look at unique byte sequences

# Try to find ASIS{ pattern by frequency analysis
# Most common 2-byte sequences
print("\nLooking for pattern structure...")

# Split into groups and analyze
# The pattern "��,D��ҺV&j��" repeats
# This might be the encoding of common words

# Let me try reverse engineering - if this is substitution
# The file should contain "ASIS{" somewhere
# Let's build a mapping by assuming certain patterns

# Common 5-char sequence for "ASIS{" 
# Let me extract the beginning pattern

beginning = text[:50]
print(f"\nBeginning text: {repr(beginning)}")

# Try to decode assuming it's a simple character substitution
# Build frequency-based mapping

# Let's try a more direct approach - check if this is actually a different encoding
print("\nTrying different decodings...")

# Check if it might be in a specific Persian/Arabic encoding
import codecs

for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'utf-32', 'cp1256', 'iso-8859-6']:
    try:
        decoded = data.decode(encoding, errors='ignore')
        if 'ASIS' in decoded or 'asis' in decoded or 'flag' in decoded:
            print(f"\nFOUND with {encoding}:")
            print(decoded[:500])
            with open(f'decoded_{encoding}.txt', 'w', encoding='utf-8') as f:
                f.write(decoded)
    except:
        pass

# If that doesn't work, try character mapping
# Looking at the view output, common sequences are:
# "D,ҺV&j" "ؔ66" "بD" etc.

# These might map to common English letters
# Let's build a mapping

print("\nBuilding substitution map...")

# Create a sorted list of characters by frequency
sorted_chars = [char for char, count in sorted(freq.items(), key=lambda x: -x[1]) if char.strip()]

# Common English letter frequency: ETAOINSHRDLCUMWFGYPBVKJXQZ
# For a flag, we'd expect different distribution

# Let me try assuming the most common is a space
mapping = {}

# Check for patterns that might be word boundaries
import re

# Look for repeated short sequences that might be common words
words = text.split()[:20]
print(f"\nFirst 20 'words': {words}")

# Manual mapping attempt - if I can find "ASIS{" pattern
# Let me check if there's a simpler pattern

print("\n\nAttempting frequency-based substitution...")
# Most common char in English text is space, then 'e', 't', 'a'...

english_freq = ' etaoinshrdlcumwfgypbvkjxqz0123456789_-{}!ETAOINSHRDLCUMWFGYPBVKJXQZ'
result = []

for char in text:
    idx = sorted_chars.index(char) if char in sorted_chars else -1
    if idx >= 0 and idx < len(english_freq):
        result.append(english_freq[idx])
    else:
        result.append('?')

decoded_text = ''.join(result)
print(decoded_text[:500])

# Save result
with open('decoded_freq.txt', 'w', encoding='utf-8') as f:
    f.write(decoded_text)

# Search for ASIS pattern
if 'ASIS' in decoded_text or 'asis' in decoded_text.lower():
    import re
    flags = re.findall(r'ASIS\{[^}]+\}', decoded_text, re.IGNORECASE)
    if flags:
        print(f"\n\nFLAG FOUND: {flags[0]}")
