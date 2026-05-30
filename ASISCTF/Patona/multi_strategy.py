# Manual analysis of flag.raw based on visible patterns

# From the view, I saw these repeating patterns:
# ",D��ҺV&j��ؔ66�j��j&V,D�ؔ6�D,Һ&V��,D���بҺVV��D,ҺV&j��j&V��,D�ؔ66�ب"
#
# Characters identified:
# Latin: D, V, j, & , (comma), 6
# Arabic: ب (U+0628), د (U+062F), ر (U+0631), ز (U+0632), ظ (U+0638)
#         Һ (U+04BA - Cyrillic), ؔ (U+0614), ج (U+062C)
#         x (U+0078), u (U+0075), t (U+0074), z (U+007A)

# This is clearly a substitution cipher using Unicode characters
# Let me create a mapping based on frequency and context

def main():
    with open('flag.raw', 'rb') as f:
        data = f.read()
    
    # Decode
    text = data.decode('utf-8')
    
    # Count frequency
    from collections import Counter
    freq = Counter(text)
    
    # Most common characters (from analysis)
    # Should map to space and common letters
    
    sorted_chars = [c for c, _ in freq.most_common()]
    
    # English frequency: space, e, t, a, o, i, n, s, h, r, d, l, c, u...
    # But for CTF flags, might be: {, }, _, a, e, i, o, n, r, s, t...
    
    # Build mapping - try different strategies
    strategies = [
        # Strategy 1: Standard English frequency
        ' etaoinsrhdlcumwfgypbvkxjqz_0123456789ETAOINSRHDLCUMWFGYPBVKXJQZ-{},.;:!?',
        # Strategy 2: Code/flag optimized
        ' _etaoinsrhdlcumwfgypbvkxjqz0123456789{}ETAOINSRHDLCUMWFGYPBVKXJQZ-,.;:!?',
        # Strategy 3: Start with common flag chars
        '{}ASIS_abcdefghijklmnopqrstuvwxyz0123456789 ETAOINSRHDLCUMWFGYPBVKXJQZ-,.;:!?',
    ]
    
    for strategy_num, eng_freq_list in enumerate(strategies, 1):
        print(f"\n{'='*70}")
        print(f"STRATEGY {strategy_num}")
        print(f"{'='*70}")
        
        mapping = {}
        for i, ch in enumerate(sorted_chars):
            if i < len(eng_freq_list):
                mapping[ch] = eng_freq_list[i]
            else:
                mapping[ch] = '?'
        
        # Decode
        decoded = ''.join(mapping.get(c, c) for c in text)
        
        # Show sample
        print(f"First 500 characters:")
        print(decoded[:500])
        
        # Search for flag
        if 'ASIS{' in decoded or 'asis{' in decoded.lower():
            print(f"\n{'*'*70}")
            print(f"FOUND FLAG PATTERN IN STRATEGY {strategy_num}!")
            print(f"{'*'*70}")
            
            # Extract flag
            import re
            flags = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
            if flags:
                print(f"\nFLAG: {flags[0]}")
                return
        
        # Save this attempt
        with open(f'decode_strategy{strategy_num}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Strategy {strategy_num} mapping:\n")
            f.write(f"Frequency string: {eng_freq_list}\n\n")
            f.write(decoded)
    
    print("\n\nNo obvious flag found. Saved all attempts to decode_strategy*.txt files.")
    print("Manual analysis may be needed.")

if __name__ == '__main__':
    main()
