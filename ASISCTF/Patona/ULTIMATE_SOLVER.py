#!/usr/bin/env python3
"""
ULTIMATE PATONA SOLVER
Tries multiple decryption strategies systematically
"""

import re
from collections import Counter

def read_file():
    """Read and return both binary and text versions"""
    with open('flag.raw', 'rb') as f:
        data = f.read()
    text = data.decode('utf-8', errors='replace')
    return data, text

def frequency_substitution(text, alphabet):
    """Apply frequency-based substitution cipher"""
    char_freq = Counter(text)
    chars_sorted = [ch for ch, _ in char_freq.most_common()]
    
    substitution = {}
    for idx, source_char in enumerate(chars_sorted):
        if idx < len(alphabet):
            substitution[source_char] = alphabet[idx]
        else:
            substitution[source_char] = '?'
    
    return ''.join(substitution.get(c, c) for c in text)

def find_flags(text):
    """Search for ASIS{...} patterns"""
    pattern = r'ASIS\{[^}]{5,150}\}'
    return re.findall(pattern, text, re.IGNORECASE)

def try_xor(data, key):
    """Try XOR decryption"""
    if isinstance(key, int):
        key = bytes([key])
    
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    
    try:
        return bytes(result).decode('utf-8', errors='ignore')
    except:
        return None

def main():
    print("="*80)
    print("PATONA CHALLENGE SOLVER")
    print("="*80)
    
    # Read data
    data, text = read_file()
    print(f"\nFile size: {len(data)} bytes")
    print(f"Text length: {len(text)} characters")
    
    # Show character frequency
    char_freq = Counter(text)
    print(f"Unique characters: {len(char_freq)}\n")
    
    print("Top 30 characters by frequency:")
    for i, (ch, cnt) in enumerate(char_freq.most_common(30)):
        print(f"{i:2d}. '{ch}' (U+{ord(ch):04X}): {cnt:5d}")
    
    # ===== STRATEGY 1: Standard frequency analysis =====
    print("\n" + "="*80)
    print("STRATEGY 1: Standard English Frequency")
    print("="*80)
    
    alphabet1 = ' etaoinsrhldcumfgypbvkxjqzETAOINSRHLDCUMFGYPBVKXJQZ0123456789_-.,;:!?()[]{}"\'/\\@#$%^&*+=<>|`~'
    decoded1 = frequency_substitution(text, alphabet1)
    print(decoded1[:1500])
    
    flags1 = find_flags(decoded1)
    if flags1:
        print("\n" + "*"*80)
        print("FLAGS FOUND:")
        for flag in flags1:
            print(f"  {flag}")
        print("*"*80)
        with open('FLAG_SOLUTION.txt', 'w') as f:
            f.write(f"{flags1[0]}\n")
        return flags1[0]
    
    # ===== STRATEGY 2: Flag-priority mapping =====
    print("\n" + "="*80)
    print("STRATEGY 2: Flag Characters Priority")
    print("="*80)
    
    alphabet2 = 'ASIS{} _etaoinsrhldcumfgypbvkxjqzETOINRHLDCUMFGYPBVKXJQZ0123456789-.,;:!?()[]"\'/\\@#$%^&*+=<>|`~'
    decoded2 = frequency_substitution(text, alphabet2)
    print(decoded2[:1500])
    
    flags2 = find_flags(decoded2)
    if flags2:
        print("\n" + "*"*80)
        print("FLAGS FOUND:")
        for flag in flags2:
            print(f"  {flag}")
        print("*"*80)
        with open('FLAG_SOLUTION.txt', 'w') as f:
            f.write(f"{flags2[0]}\n")
        return flags2[0]
    
    # ===== STRATEGY 3: XOR with single byte =====
    print("\n" + "="*80)
    print("STRATEGY 3: Single-byte XOR")
    print("="*80)
    
    for key_byte in range(256):
        decoded3 = try_xor(data, key_byte)
        if decoded3:
            flags3 = find_flags(decoded3)
            if flags3:
                print(f"\nFOUND with XOR key 0x{key_byte:02x}:")
                print(decoded3[:500])
                print("\n" + "*"*80)
                print(f"FLAG: {flags3[0]}")
                print("*"*80)
                with open('FLAG_SOLUTION.txt', 'w') as f:
                    f.write(f"{flags3[0]}\n")
                return flags3[0]
    
    # ===== STRATEGY 4: Multi-byte XOR =====
    print("\n" + "="*80)
    print("STRATEGY 4: Multi-byte XOR")
    print("="*80)
    
    common_keys = [
        b'ASIS', b'patona', b'Patona', b'PATONA',
        b'flag', b'FLAG', b'key', b'secret', b'password',
        b'crypto', b'ctf', b'CTF', b'asis'
    ]
    
    for key in common_keys:
        decoded4 = try_xor(data, key)
        if decoded4:
            flags4 = find_flags(decoded4)
            if flags4:
                print(f"\nFOUND with key {key}:")
                print(decoded4[:500])
                print("\n" + "*"*80)
                print(f"FLAG: {flags4[0]}")
                print("*"*80)
                with open('FLAG_SOLUTION.txt', 'w') as f:
                    f.write(f"{flags4[0]}\n")
                return flags4[0]
    
    # ===== STRATEGY 5: Reverse mapping (least frequent = ASIS) =====
    print("\n" + "="*80)
    print("STRATEGY 5: Reverse Frequency (rare chars = flag chars)")
    print("="*80)
    
    chars_sorted_rev = [ch for ch, _ in sorted(char_freq.items(), key=lambda x: x[1])]
    alphabet5 = 'ASIS{}_'
    extended5 = 'etaoinsrhldcumfgypbvkxjqz0123456789-.,;:!?()[]"\'/\\@#$%^&*+=<>|`~ETAOINSRHLDCUMFGYPBVKXJQZ'
    full_alpha5 = alphabet5 + extended5
    
    substitution5 = {}
    for idx, source_char in enumerate(chars_sorted_rev):
        if idx < len(full_alpha5):
            substitution5[source_char] = full_alpha5[idx]
        else:
            substitution5[source_char] = '?'
    
    decoded5 = ''.join(substitution5.get(c, c) for c in text)
    print(decoded5[:1500])
    
    flags5 = find_flags(decoded5)
    if flags5:
        print("\n" + "*"*80)
        print("FLAGS FOUND:")
        for flag in flags5:
            print(f"  {flag}")
        print("*"*80)
        with open('FLAG_SOLUTION.txt', 'w') as f:
            f.write(f"{flags5[0]}\n")
        return flags5[0]
    
    # ===== SAVE ALL ATTEMPTS =====
    print("\n\nSaving all decoded attempts for manual review...")
    with open('decode_attempt1.txt', 'w', encoding='utf-8') as f:
        f.write(decoded1)
    with open('decode_attempt2.txt', 'w', encoding='utf-8') as f:
        f.write(decoded2)
    with open('decode_attempt5.txt', 'w', encoding='utf-8') as f:
        f.write(decoded5)
    
    print("Saved to: decode_attempt1.txt, decode_attempt2.txt, decode_attempt5.txt")
    print("\n[No flag found automatically - manual review required]")
    return None

if __name__ == '__main__':
    result = main()
    if result:
        print(f"\n\n{'='*80}")
        print(f"FINAL ANSWER: {result}")
        print(f"{'='*80}")
    else:
        print("\n\nNo flag found. Check the decode_attempt*.txt files manually.")
