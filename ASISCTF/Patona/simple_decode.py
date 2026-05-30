#!/usr/bin/env python3
import sys
import os

# Basic script that should work even with minimal Python
try:
    # Read file
    with open('flag.raw', 'rb') as f:
        raw_data = f.read()
    
    # Decode UTF-8
    text = raw_data.decode('utf-8', errors='replace')
    
    # Get unique characters and their counts
    char_counts = {}
    for ch in text:
        char_counts[ch] = char_counts.get(ch, 0) + 1
    
    # Sort by frequency  
    sorted_chars = sorted(char_counts.items(), key=lambda x: -x[1])
    
    print(f"File has {len(text)} characters, {len(char_counts)} unique")
    print("\nTop 30 most frequent characters:")
    print("-" * 60)
    for i, (ch, count) in enumerate(sorted_chars[:30]):
        hex_val = f"U+{ord(ch):04X}"
        print(f"{i:2d}. {hex_val} '{ch}' : {count:6d} occurrences")
    
    print("\n" + "=" * 60)
    print("Attempting frequency substitution cipher decode...")
    print("=" * 60)
    
    # English letter frequency for comparison (most common first)
    # Including common flag characters
    eng_freq = ' etaoinshrdlcumwfgypbvkjxqz0123456789_-ETAOINSHRDLCUMWFGYPBVKJXQZ{},:;.!?'
    
    # Build mapping dictionary
    char_map = {}
    for i, (ch, count) in enumerate(sorted_chars):
        if i < len(eng_freq):
            char_map[ch] = eng_freq[i]
        else:
            char_map[ch] = '?'
    
    # Apply the mapping
    decoded = ''
    for ch in text:
        decoded += char_map.get(ch, ch)
    
    # Display first part
    print("\nDecoded text (first 1000 characters):")
    print("-" * 60)
    print(decoded[:1000])
    
    # Look for ASIS pattern
    print("\n" + "=" * 60)
    print("Searching for flag patterns...")
    print("=" * 60)
    
    decoded_lower = decoded.lower()
    
    # Search for 'asis{'
    if 'asis{' in decoded_lower:
        idx = decoded_lower.find('asis{')
        # Find the closing brace
        end_idx = decoded_lower.find('}', idx)
        if end_idx > idx:
            potential_flag = decoded[idx:end_idx+1]
            print(f"\n*** POTENTIAL FLAG FOUND ***")
            print(f"{potential_flag}")
            print("=" * 60)
    
    # Also look for any {...} patterns
    import re
    braced_patterns = re.findall(r'\{[^}]{5,}\}', decoded)
    if braced_patterns:
        print(f"\nFound {len(braced_patterns)} braced patterns:")
        for i, pattern in enumerate(braced_patterns[:10]):
            print(f"  {i+1}. ...{pattern}")
    
    # Look for 4-letter-word followed by {
    flag_patterns = re.findall(r'[A-Za-z]{4}\{[^}]+\}', decoded)
    if flag_patterns:
        print(f"\nPotential flag formats found:")
        for pattern in flag_patterns:
            print(f"  {pattern}")
    
    # Write full decoded text to file
    with open('decoded_flag.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
    
    print(f"\nFull decoded text saved to: decoded_flag.txt")
    print(f"Total decoded length: {len(decoded)} characters")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\nScript completed.")
