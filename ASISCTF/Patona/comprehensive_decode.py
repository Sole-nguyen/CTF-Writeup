#!/usr/bin/env python3
"""
Byte-level analysis and decoding for Patona challenge
"""
import struct
import binascii

def analyze_bytes():
    with open('flag.raw', 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    print(f"\nFirst 100 bytes (hex):")
    print(binascii.hexlify(data[:100]).decode())
    print(f"\nFirst 100 bytes (decimal):")
    print([data[i] for i in range(min(100, len(data)))])
    
    # Frequency analysis at byte level
    byte_freq = {}
    for byte in data:
        byte_freq[byte] = byte_freq.get(byte, 0) + 1
    
    print(f"\n\nByte frequency analysis (top 30):")
    print("Rank | Hex  | Dec | ASCII | Count")
    print("-" * 50)
    sorted_bytes = sorted(byte_freq.items(), key=lambda x: -x[1])
    for i, (byte, count) in enumerate(sorted_bytes[:30]):
        ascii_char = chr(byte) if 32 <= byte < 127 else '.'
        print(f"{i:4d} | 0x{byte:02x} | {byte:3d} | '{ascii_char}'   | {count:6d}")
    
    # Try XOR with single byte
    print("\n\nTrying single-byte XOR decryption...")
    for key in range(256):
        decoded = bytes([b ^ key for b in data])
        try:
            text = decoded.decode('utf-8', errors='ignore')
            if 'ASIS{' in text or 'flag{' in text.lower():
                print(f"\n*** FOUND with XOR key 0x{key:02x} ({key}) ***")
                print(text[:500])
                
                # Extract flag
                import re
                flags = re.findall(r'ASIS\{[^}]+\}', text, re.IGNORECASE)
                if flags:
                    print(f"\n{'*'*70}")
                    print(f"FLAG: {flags[0]}")
                    print(f"{'*'*70}")
                    with open('FOUND_FLAG.txt', 'w') as f:
                        f.write(flags[0])
                return True
        except:
            pass
    
    # Try multi-byte XOR with common keys
    print("\nTrying multi-byte XOR with common keys...")
    common_keys = [b'ASIS', b'FLAG', b'flag', b'patona', b'Patona', b'PATONA', 
                   b'key', b'secret', b'password', b'ctf', b'CTF']
    
    for key in common_keys:
        decoded = bytearray()
        for i, byte in enumerate(data):
            decoded.append(byte ^ key[i % len(key)])
        
        try:
            text = bytes(decoded).decode('utf-8', errors='ignore')
            if 'ASIS{' in text or 'flag' in text.lower():
                print(f"\n*** FOUND with key {key} ***")
                print(text[:500])
                
                import re
                flags = re.findall(r'ASIS\{[^}]+\}', text, re.IGNORECASE)
                if flags:
                    print(f"\nFLAG: {flags[0]}")
                    return True
        except:
            pass
    
    # Check if it's UTF-16 or other encoding
    print("\nTrying alternative encodings...")
    for encoding in ['utf-16-le', 'utf-16-be', 'utf-32-le', 'utf-32-be', 
                     'cp1256', 'iso-8859-6', 'windows-1256']:
        try:
            text = data.decode(encoding, errors='ignore')
            if 'ASIS' in text or 'flag' in text.lower():
                print(f"\n*** FOUND with encoding {encoding} ***")
                print(text[:500])
                
                import re
                flags = re.findall(r'ASIS\{[^}]+\}', text, re.IGNORECASE)
                if flags:
                    print(f"\nFLAG: {flags[0]}")
                    return True
        except:
            pass
    
    return False

def substitution_decode():
    """Try substitution cipher on UTF-8 decoded text"""
    with open('flag.raw', 'rb') as f:
        data = f.read()
    
    text = data.decode('utf-8', errors='replace')
    
    print("\n\n" + "="*70)
    print("SUBSTITUTION CIPHER ANALYSIS")
    print("="*70)
    
    from collections import Counter
    freq = Counter(text)
    sorted_chars = [c for c, _ in freq.most_common()]
    
    print(f"Unique characters: {len(sorted_chars)}")
    
    # Try multiple frequency mappings
    attempts = [
        (' etaoinsrhdlcumwfgypbvkxjqz', 'Standard English'),
        ('etaoin srhldcumwfgypbvkxjqz', 'English (e first)'),
        (' _{}etaoinsrhdlcumwfgypbvkxjqz', 'Code-optimized'),
        ('ASIS{}_abcdefghijklmnopqrstuvwxyz0123456789 ', 'Flag-first'),
    ]
    
    for freq_str, description in attempts:
        # Extend freq_str to cover all characters
        extended = freq_str + '0123456789-,.;:!?()[]<>@#$%^&*+=~/\\|`"\' \t\n'
        extended += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        extended += ''.join(chr(i) for i in range(128, 256))
        
        mapping = {}
        for i, ch in enumerate(sorted_chars):
            if i < len(extended):
                mapping[ch] = extended[i]
            else:
                mapping[ch] = '?'
        
        decoded = ''.join(mapping.get(c, c) for c in text)
        
        # Check for flag
        if 'ASIS{' in decoded or 'asis{' in decoded.lower():
            print(f"\n*** FOUND with {description} mapping! ***")
            print(decoded[:700])
            
            import re
            flags = re.findall(r'ASIS\{[^}]+\}', decoded, re.IGNORECASE)
            if flags:
                print(f"\n{'*'*70}")
                print(f"FLAG: {flags[0]}")
                print(f"{'*'*70}")
                return True
    
    return False

if __name__ == '__main__':
    print("Starting analysis...\n")
    
    if not analyze_bytes():
        print("\n Byte-level analysis didn't find flag.")
        print("Trying substitution cipher...")
        
        if not substitution_decode():
            print("\nNo flag found. Manual analysis required.")
            print("Check the generated output files.")
    
    print("\nAnalysis complete.")
