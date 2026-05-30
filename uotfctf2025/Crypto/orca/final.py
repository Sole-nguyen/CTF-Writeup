#!/usr/bin/env python3
"""
ORCA Final Exploit

The key: ECB mode + block shuffling with fixed permutation.

If we send input where we can identify specific blocks, we can reverse
the permutation and reconstruct the plaintext!

Strategy:
1. Send input with 16 unique blocks (each block has unique pattern)
2. Query all 65 shuffled blocks
3. Identify which shuffled position each original block went to
4. Send minimal input and query all blocks
5. Reverse the shuffle to get original plaintext
6. Extract flag from plaintext
"""

import socket
import base64
from Crypto.Cipher import AES

BS = 16
n = 65

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    return s

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

def find_permutation(s):
    """
    Find the permutation by sending 16 unique identifiable blocks.
    """
    print("[*] Finding shuffle permutation...")
    
    # Create 16 unique blocks (we can fit 256 bytes = 16 blocks in user input)
    # Each block will have a unique pattern we can identify
    unique_blocks = []
    for i in range(16):
        # Pattern: [i, i, i, ...] repeated 16 times
        block = bytes([i] * 16)
        unique_blocks.append(block)
    
    test_input = b''.join(unique_blocks)
    
    # Encrypt these blocks locally to know what they should look like
    # Wait, we don't know the key. But we can identify them by querying.
    
    # Different approach: use blocks that create predictable encrypted patterns
    # Actually, we CAN identify them! Each block encrypts to something unique.
    
    # Query all blocks with our unique input
    print("    Querying all blocks with unique input...")
    shuffled_blocks = {}
    for idx in range(n):
        enc = query(s, idx, test_input)
        if enc:
            shuffled_blocks[idx] = enc
    
    print(f"    Collected {len(shuffled_blocks)} shuffled blocks")
    
    # Now we need to figure out which shuffled block corresponds to which original block
    # We know blocks 0-15 (after prefix) should be our unique blocks
    # But we don't know the prefix length...
    
    # Let's try sending single unique blocks and seeing where they appear
    print("    Mapping individual blocks...")
    
    # Send just one block type and see where it appears
    single_block_queries = {}
    for i in range(16):
        test_single = bytes([i] * 16) * 16  # Fill all 256 bytes with same block
        
        # Query a few indices to find the repeated encrypted block
        sample_enc = None
        for idx in [0, 5, 10]:
            enc = query(s, idx, test_single)
            if enc:
                sample_enc = enc
                break
        
        if sample_enc:
            # Find all indices that have this encrypted block
            matching_indices = []
            for idx, enc in shuffled_blocks.items():
                if enc == sample_enc:
                    matching_indices.append(idx)
            
            if matching_indices:
                print(f"      Block pattern {i}: appears at shuffled indices {matching_indices[:5]}")
                single_block_queries[i] = (sample_enc, matching_indices)
    
    return shuffled_blocks, single_block_queries

def exploit():
    s = connect()
    
    # Find permutation (this will take some queries)
    shuffled, mappings = find_permutation(s)
    
    # Now query with minimal input to get flag
    print("\n[*] Querying with minimal input to extract flag...")
    flag_blocks = {}
    minimal_input = b""  # Or maybe a few bytes to align
    
    for idx in range(n):
        enc = query(s, idx, minimal_input)
        if enc:
            flag_blocks[idx] = enc
    
    # Try to decrypt or identify flag blocks
    # Since we can't decrypt without the key, we need a different approach
    
    print("[*] Collecting blocks with known plaintext...")
    
    # Let's try: send "uoftctf{" repeated and see if we can match
    known = b"uoftctf{" * 32  # Fill 256 bytes
    known_blocks = {}
    for idx in range(n):
        enc = query(s, idx, known)
        if enc:
            known_blocks[idx] = enc
    
    # Compare with minimal input to find differences
    print(f"\n[*] Comparing blocks...")
    for idx in range(min(20, n)):
        if idx in flag_blocks and idx in known_blocks:
            same = "SAME" if flag_blocks[idx] == known_blocks[idx] else "DIFF"
            print(f"    Block {idx}: {same}")
            if same == "SAME":
                print(f"      -> This block might contain 'uoftctf{'!")
    
    s.close()
    return None

if __name__ == "__main__":
    exploit()
