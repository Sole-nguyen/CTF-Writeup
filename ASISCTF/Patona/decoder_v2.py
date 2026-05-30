#!/usr/bin/env python3
"""
Patona Challenge - Reverse the Arabic character substitution
The challenge appears to use Arabic characters as a substitution cipher
"""

# Read the encrypted flag
with open('flag.raw', 'rb') as f:
    encrypted = f.read().decode('utf-8')

# I noticed these Persian/Arabic characters in the pattern:
# ب ت ج د ر ز س ش ص ض ط ظ ع خ ذ
# These are letters from the Arabic alphabet

# The challenge name "Patona" might be a hint
# Let me check if it's a simple ROT or substitution

# Analysis of the characters shows:
# Arabic chars are being used to represent Latin alphabet

# Build a mapping based on common patterns
# Looking at "ASIS{" pattern, I need to find 5-char sequences

print("Decoding...")

# From looking at the file, common patterns are:
# ,D ҺV &j ؔ6 بD 

# These seem to encode common letters
# Let me try to map Persian alphabet to English

# Persian/Arabic alphabet commonly used letters:
persian = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
# The challenge might use a subset

# Alternative: Check if it's using Unicode positions offset
result = []
for char in encrypted:
    code = ord(char)
    # Try different offsets
    if code >= 0x600:  # Arabic range starts around 0x600
        # Calculate offset from Arabic 'alef' (first letter)
        offset = code - 0x627  # ا is U+0627
        if -26 <= offset <= 26:
            # Map to English letter
            if offset >= 0:
                result.append(chr(ord('a') + (offset % 26)))
            else:
                result.append(chr(ord('A') + ((-offset) % 26)))
        else:
            result.append(char)
    else:
        result.append(char)

decoded = ''.join(result)
print("Attempt 1:")
print(decoded[:200])

if 'ASIS{' in decoded or 'asis{' in decoded.lower():
    # Extract flag
    import re
    matches = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
    if matches:
        print(f"\n*** FLAG FOUND: {matches[0]} ***")

# Try another approach - maybe it's simpler
# Check if certain characters directly map to A, S, I, {, }

from collections import Counter
freq = Counter(encrypted)

print("\n\nMost common characters:")
common_chars = [ch for ch, cnt in freq.most_common(40)]
for i, ch in enumerate(common_chars[:20]):
    print(f"{i}: '{ch}' U+{ord(ch):04X} count:{freq[ch]}")

# Now let me try a smarter mapping
# If we assume standard frequency analysis:
# Most common should be space or 'e'

print("\n\nTrying frequency analysis...")

# English letter frequency (including space and common chars)
eng_freq = list(' etaoinshrdlucmfwypvbgkjqxz_-.,{}!?1234567890ETAOINSHRDLUCMFWYPVBGKJQXZ')

# Build mapping
char_map = {}
for i, char in enumerate(common_chars):
    if i < len(eng_freq):
        char_map[char] = eng_freq[i]

# Apply mapping
decoded2 = ''.join(char_map.get(ch, ch) for ch in encrypted)
print(decoded2[:300])

# Search for flag pattern
if 'asis{' in decoded2.lower():
    import re
    matches = re.findall(r'asis\{[^}]*\}', decoded2, re.IGNORECASE)
    for m in matches:
        print(f"\n*** POTENTIAL FLAG: {m} ***")

# Save for inspection
with open('decoded_output.txt', 'w', encoding='utf-8') as f:
    f.write("=== Original (first 1000) ===\n")
    f.write(encrypted[:1000])
    f.write("\n\n=== Decoded Attempt 1 (first 1000) ===\n")
    f.write(decoded[:1000])
    f.write("\n\n=== Decoded Attempt 2 (first 1000) ===\n")
    f.write(decoded2[:1000])
    f.write("\n\n=== Full Decoded Attempt 2 ===\n")
    f.write(decoded2)

print("\nOutput saved to decoded_output.txt")
