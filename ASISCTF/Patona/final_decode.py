#!/usr/bin/env python3
"""
Final decoder for Patona challenge
Based on the visible patterns, this uses Arabic script substitution
"""

# The patterns I saw in the file:
# ب د ر ز س ش خ ت ج etc. - Arabic letters
# Also: D , Һ V & j ؔ 6

# This appears to be using a mix of:
# 1. Arabic letters  
# 2. Latin letters (D, V, j)
# 3. Punctuation (, &)
# 4. Numbers (6)
# 5. Special chars (Һ, ؔ)

with open('flag.raw', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')

# Let me build a character mapping based on what I observed
# The key insight: certain character combinations represent English letters

# From the repeating pattern ",D�ؔ66�بD,ҺV&j��j&V��,D�ؔ66�ب"
# This likely encodes common words or parts of the flag

# Let me try a direct character-to-character mapping
# Based on frequency and the ASIS{ pattern

# Build frequency table first
from collections import Counter
freq = Counter(text)
sorted_by_freq = [ch for ch, _ in freq.most_common()]

print(f"Total characters: {len(text)}")
print(f"Unique characters: {len(freq)}")
print("\nTop 20 characters by frequency:")
for i, ch in enumerate(sorted_by_freq[:20]):
    print(f"  {i:2d}. U+{ord(ch):04X} '{ch}' : {freq[ch]:6d} times")

# Expected flag format: ASIS{...}
# So we need to map to: A, S, I, {, }

# Strategy: The challenge name is "Patona"  
# This might mean "Pattern" or be a cipher name

# Let me try mapping the most frequent characters to common English:
# In normal English: space, e, t, a, o, i, n, s, r, h...
# But in code/flags: _, a, e, i, o, n, r, s, t, l, c...

# Try simple substitution
mapping_attempt = {
    # Will map based on analysis
}

# Alternative: Check if consecutive bytes form a pattern
# The Arabic Unicode range is U+0600 to U+06FF
# Latin is U+0041-U+005A (A-Z) and U+0061-U+007A (a-z)

# Simple offset cipher check
for offset in [0x600 - ord('A'), 0x600 - ord('a'), 0x627 - ord('A'), 0x627 - ord('a')]:
    result = []
    for ch in text:
        code = ord(ch)
        if 0x600 <= code <= 0x6FF:  # Arabic range
            new_code = code - offset
            if ord('A') <= new_code <= ord('Z') or ord('a') <= new_code <= ord('z'):
                result.append(chr(new_code))
            else:
                result.append('?')
        elif ord('A') <= code <= ord('Z') or ord('a') <= code <= ord('z'):
            result.append(ch)
        elif ch in '{}[]:;_-,.!? \n\t0123456789':
            result.append(ch)
        else:
            result.append('*')
    
    decoded = ''.join(result)
    if 'ASIS{' in decoded or 'asis{' in decoded.lower():
        print(f"\n\n*** FOUND WITH OFFSET {offset} ***")
        print(decoded)
        import re
        flags = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
        if flags:
            print(f"\n\n*** FLAG: {flags[0]} ***")
            break
else:
    print("\nSimple offset didn't work. Trying substitution...")
    
    # Manual substitution based on the pattern structure
    # Map Arabic letters to English in alphabetical order
    arabic_letters = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوي'
    english = 'abcdefghijklmnopqrstuvwxyz'
    
    # Extend to cover more chars
    all_chars = sorted(set(text))
    print(f"\nAll unique characters ({len(all_chars)}):")
    print(''.join(all_chars[:50]))
    
    # Build a smarter mapping
    # Let's map the most common character to space
    mapping = {}
    
    # Map top freq chars to: space, e, t, a, o, i, n, s, h, r, d, l, u
    common_eng = ' etaoinsrhldcumfpgwybvkxjqz_-,.:;!?{}[]()0123456789'
    
    for i, ch in enumerate(sorted_by_freq):
        if i < len(common_eng):
            mapping[ch] = common_eng[i]
        else:
            mapping[ch] = '?'
    
    decoded2 = ''.join(mapping.get(ch, ch) for ch in text)
    
    print("\n\nFrequency-based decode (first 500 chars):")
    print(decoded2[:500])
    
    # Search for flag-like patterns
    import re
    # Look for ASIS{ or similar patterns
    potential = re.findall(r'[A-Z]{4}\{[^}]{10,100}\}', decoded2)
    if potential:
        print(f"\n*** POTENTIAL FLAGS: ***")
        for p in potential:
            print(f"  {p}")
    
    # Save full output
    with open('final_decode.txt', 'w', encoding='utf-8') as f:
        f.write(decoded2)
    print("\nFull decode saved to final_decode.txt")

print("\nDone!")
