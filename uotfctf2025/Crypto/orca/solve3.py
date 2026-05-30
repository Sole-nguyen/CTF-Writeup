#!/usr/bin/env python3
"""
ORCA Exploit - ECB Block Recovery

Since the permutation is fixed per connection but blocks contain random data,
we need a different approach. The key insight:

1. Message = prefix(random, 0-96) + user_input(≤256) + FLAG + random_padding
2. Total = 1024 bytes → 1040 with PKCS7 → 65 blocks
3. Blocks are shuffled with a FIXED permutation per connection
4. ECB mode = same plaintext → same ciphertext

Attack: Build a dictionary by controlling input to create known plaintext blocks,
then match those to find where they appear after shuffling.
"""

import socket
import base64
from collections import defaultdict

BS = 16
n = 65

def query(s, idx, data=b""):
    req = f"{idx}:{data.hex()}\n" if data else f"{idx}\n"
    s.sendall(req.encode())
    resp = s.recv(4096).decode()
    
    for line in resp.split('\n'):
        line = line.strip()
        if line and line not in ['>', 'error']:
            try:
                return base64.b64decode(line)
            except:
                pass
    return None

def find_controlled_blocks(s):
    """
    Find which block indices we can control by using repeated patterns.
    """
    print("[*] Finding controlled blocks using repeated patterns...")
    
    # Create input with 16 identical blocks (each "AAAA..."*16)
    block_A = b'A' * 16
    input_all_A = block_A * 16  # 256 bytes
    
    # Query all indices
    enc_blocks_A = {}
    for idx in range(n):
        enc = query(s, idx, input_all_A)
        if enc:
            enc_blocks_A[idx] = enc
    
    # Now use different pattern to see which blocks we control
    block_B = b'B' * 16
    input_all_B = block_B * 16
    
    enc_blocks_B = {}
    for idx in range(n):
        enc = query(s, idx, input_all_B)
        if enc:
            enc_blocks_B[idx] = enc
    
    # Blocks that changed are under our control
    controlled = []
    for idx in range(n):
        if idx in enc_blocks_A and idx in enc_blocks_B:
            if enc_blocks_A[idx] != enc_blocks_B[idx]:
                controlled.append(idx)
    
    print(f"    Found {len(controlled)} controlled block indices: {controlled[:20]}")
    
    # Also find which indices give us the encrypted 'AAAA...' block
    enc_A = None
    enc_B = None
    
    # Count frequency of each encrypted block value
    freq_A = defaultdict(list)
    for idx, enc in enc_blocks_A.items():
        freq_A[enc].append(idx)
    
    # Blocks that appear multiple times are likely our repeated pattern
    for enc, indices in freq_A.items():
        if len(indices) >= 2:  # Appears at least twice = likely our repeated block
            print(f"    Encrypted block {base64.b64encode(enc).decode()} appears at indices: {indices[:10]}")
            if enc_A is None:
                enc_A = enc
    
    return controlled, enc_A, enc_blocks_A

def extract_flag_with_dictionary(s):
    """
    Extract flag by building a dictionary attack.
    """
    print("\n[*] Starting dictionary-based flag extraction...")
    
    # Step 1: Find blocks we control
    controlled, enc_ref, _ = find_controlled_blocks(s)
    
    if not controlled:
        print("[-] Could not find controlled blocks!")
        return None
    
    # Step 2: Build byte-by-byte dictionary
    # We'll try to find flag by:
    # 1. Using input to push known_flag into a block
    # 2. Brute forcing the next byte
    # 3. Matching against encrypted blocks we can query
    
    flag = bytearray(b"uoftctf{")  # Known prefix
    
    print(f"\n[*] Starting with known prefix: {flag.decode()}")
    
    max_flag_len = 60
    
    for pos in range(len(flag), max_flag_len):
        print(f"\n[*] Extracting byte {pos}...")
        
        found = False
        
        # We need to align things so we can brute force
        # Try different input configurations
        
        for input_len in range(0, 257 - len(flag)):
            # Build input: padding + known_flag + guess_byte
            # The goal: make (prefix + input + known_flag + guess) align to block boundary
            
            padding = b'Z' * input_len
            
            # Dictionary: guess_byte -> encrypted_block
            guess_dict = {}
            
            for guess in range(256):
                test = padding + flag + bytes([guess])
                
                # Take first 256 bytes
                if len(test) > 256:
                    test = test[:256]
                
                # Query a controlled block
                for check_idx in controlled[:5]:  # Check first few controlled indices
                    enc = query(s, check_idx, test)
                    if enc:
                        if enc not in guess_dict:
                            guess_dict[enc] = guess
                        break
            
            # Now check if any of the encrypted blocks match when we DON'T include guess
            # This means that block contains the actual flag byte
            actual_test = padding + flag
            if len(actual_test) <= 256:
                actual_test = actual_test + b'X' * (256 - len(actual_test))  # Pad to max
                
                for check_idx in controlled[:5]:
                    enc_actual = query(s, check_idx, actual_test)
                    if enc_actual and enc_actual in guess_dict:
                        found_byte = guess_dict[enc_actual]
                        flag.append(found_byte)
                        print(f"    Found byte: {chr(found_byte) if 32 <= found_byte < 127 else '?'} (0x{found_byte:02x})")
                        print(f"    Flag so far: {flag.decode(errors='ignore')}")
                        found = True
                        break
            
            if found:
                break
        
        if not found:
            print(f"    Could not find byte at position {pos}")
            
            # Check if we reached end of flag
            if b'}' in flag:
                print("\n[+] Found closing brace, flag complete!")
                break
            
            # Try a few more positions before giving up
            if pos > len(b"uoftctf{") + 5:
                break
    
    return bytes(flag)

def main():
    print("[*] Connecting to 34.186.247.84:5000")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(30)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)  # Initial prompt
    
    try:
        flag = extract_flag_with_dictionary(s)
        if flag:
            print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")
        else:
            print("\n[-] Flag extraction failed")
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        s.close()

if __name__ == "__main__":
    main()
