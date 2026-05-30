#!/usr/bin/env python3
"""
Mathematical analysis of the byte patterns
"""
import sys

def main():
    # Read data
    with open('flag.raw', 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes\n")
    
    # Key observation from the preview: many Arabic/Persian Unicode characters
    # UTF-8 encoding of Arabic is typically: 0xD8/0xD9/0xDA/0xDB followed by 0x80-0xBF
    
    # Show byte distribution
    from collections import Counter
    byte_freq = Counter(data)
    
    print("Top 20 byte values:")
    for byte_val, count in byte_freq.most_common(20):
        print(f"  0x{byte_val:02X} ({byte_val:3d}): {count:6d} times - {chr(byte_val) if 32 <= byte_val < 127 else '.'}")
    
    # Decode to text
    text = data.decode('utf-8', errors='replace')
    
    # Character frequency
    char_freq = Counter(text)
    print(f"\n\nTotal characters: {len(text)}")
    print(f"Unique characters: {len(char_freq)}\n")
    
    # List all unique characters sorted by frequency
    print("All unique characters (sorted by frequency):")
    chars_sorted = [ch for ch, _ in char_freq.most_common()]
    
    for i, ch in enumerate(chars_sorted):
        count = char_freq[ch]
        print(f"{i:3d}. '{ch}' (U+{ord(ch):04X}) : {count:6d} times", end='')
        
        # Add hint about what this might map to
        if i == 0:
            print(" <- likely SPACE or most common letter")
        elif i < 10:
            print(" <- likely common letter")
        else:
            print()
    
    # Now perform frequency-based substitution
    # ASIS{...} means we expect A, S, I, {, } to appear
    # Most likely mapping for monoalphabetic substitution:
    
    # Standard English frequency: E T A O I N S H R D L C U M W F G Y P B V K J X Q Z
    # But in code/flags: space, common letters, special chars
    
    # Strategy: Map most frequent to space, then common english letters
    english_order = ' etaoinsrhldcumfgypbvkxjqzETAOINSRHLDCUMFGYPBVKXJQZ'
    special_chars = '_-0123456789{}[]().,;:!?"\'/\\@#$%^&*+=<>|`~'
    full_alphabet = english_order + special_chars
    
    # Build the substitution table
    substitution = {}
    for idx, source_char in enumerate(chars_sorted):
        if idx < len(full_alphabet):
            substitution[source_char] = full_alphabet[idx]
        else:
            substitution[source_char] = '?'
    
    # Apply substitution
    decoded_text = ''.join(substitution.get(c, c) for c in text)
    
    print("\n" + "="*80)
    print("DECODED OUTPUT (first 3000 characters):")
    print("="*80)
    print(decoded_text[:3000])
    print("="*80)
    
    # Search for ASIS{...} pattern
    import re
    
    # Look for flag pattern
    flag_pattern = r'ASIS\{[^}]{10,150}\}'
    matches = re.findall(flag_pattern, decoded_text, re.IGNORECASE)
    
    if matches:
        print("\n" + "*"*80)
        print("FLAG(S) FOUND:")
        print("*"*80)
        for i, match in enumerate(matches, 1):
            print(f"\n{i}. {match}")
        print("\n" + "*"*80)
        
        # Save the flag
        with open('FLAG_FOUND.txt', 'w') as f:
            f.write(matches[0] + '\n')
        print(f"\nFirst flag saved to FLAG_FOUND.txt")
    else:
        print("\n[WARNING: No ASIS{...} pattern found in decoded text]")
        print("The mapping might need adjustment.")
    
    # Save full decoded text for manual review
    with open('fully_decoded.txt', 'w', encoding='utf-8') as f:
        f.write(decoded_text)
    print(f"\nFull decoded text saved to fully_decoded.txt ({len(decoded_text)} chars)")
    
    # Also try alternative mappings
    print("\n\nTrying alternative mapping (flag-priority)...")
    
    # Put ASIS{} characters at highest priority
    flag_priority = 'ASIS{}_'
    alt_alphabet = flag_priority + 'etaoinsrhldcumfgypbvkxjqzETOINRHLDCUMFGYPBVKXJQZ0123456789-.,;:!?()[]"\'/\\@#$%^&*+=<>|`~'
    
    substitution2 = {}
    for idx, source_char in enumerate(chars_sorted):
        if idx < len(alt_alphabet):
            substitution2[source_char] = alt_alphabet[idx]
        else:
            substitution2[source_char] = '?'
    
    decoded_text2 = ''.join(substitution2.get(c, c) for c in text)
    
    print("DECODED OUTPUT V2 (first 1000 characters):")
    print("-"*80)
    print(decoded_text2[:1000])
    print("-"*80)
    
    matches2 = re.findall(flag_pattern, decoded_text2, re.IGNORECASE)
    if matches2:
        print("\n" + "*"*80)
        print("FLAG(S) FOUND IN V2:")
        print("*"*80)
        for i, match in enumerate(matches2, 1):
            print(f"\n{i}. {match}")
        print("\n" + "*"*80)

if __name__ == '__main__':
    main()
