#!/usr/bin/env python3
"""
ORCA Challenge Exploit - ECB Block Oracle with Shuffling

The server:
- Takes user input u (up to 256 bytes)
- Constructs: prefix (pl bytes, 0-96) + u + FLAG + random_padding → 1024 bytes
- Encrypts with AES-ECB  
- Splits into blocks and shuffles with fixed permutation
- Returns one block at requested index

Attack: Since we can query any block and ECB is deterministic, we can:
1. Build a lookup table of encrypted blocks for known plaintexts
2. Query all blocks with different inputs to find flag blocks
3. Match encrypted blocks to recover plaintext
"""

import socket
import base64
import sys
from itertools import product

BS = 16
M = 256
L = 1024
n = L // BS + 1  # 65 blocks

def connect(host="34.186.247.84", port=5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, port))
    s.recv(1024)  # Get initial prompt
    return s

def query(s, idx, data=b""):
    """Query oracle for block at index idx with optional user input"""
    if data:
        req = f"{idx}:{data.hex()}\n"
    else:
        req = f"{idx}\n"
    
    s.sendall(req.encode())
    resp = s.recv(1024).decode().strip()
    
    # Skip prompt
    if resp.startswith('>'):
        resp = resp[1:].strip()
    
    if not resp or resp == "error":
        return None
    
    return base64.b64decode(resp)

def collect_all_blocks(s, user_input=b""):
    """Collect all 65 blocks for a given user input"""
    blocks = {}
    for idx in range(n):
        block = query(s, idx, user_input)
        if block:
            blocks[idx] = block
    return blocks

def find_flag():
    """Main attack"""
    print("[*] Connecting to oracle...")
    s = connect()
    
    print("[*] Phase 1: Collecting blocks with empty input")
    empty_blocks = collect_all_blocks(s, b"")
    print(f"    Collected {len(empty_blocks)} blocks")
    
    # The key insight: if we fill user input with known bytes,
    # we can identify which blocks are predictable
    # Then we can map out the structure
    
    print("[*] Phase 2: Collecting blocks with known input")
    known_input = b"A" * 256
    known_blocks = collect_all_blocks(s, known_input)
    
    # Compare to see which blocks changed
    changed_indices = []
    for idx in range(n):
        if idx in empty_blocks and idx in known_blocks:
            if empty_blocks[idx] != known_blocks[idx]:
                changed_indices.append(idx)
    
    print(f"    {len(changed_indices)} blocks changed when input changed")
    
    # Now let's try to extract flag using a dictionary attack
    # Build a dictionary of all possible 16-byte blocks we might see
    
    print("[*] Phase 3: Building block dictionary")
    # For each position in the flag, try to guess it
    
    # Strategy: The flag is after our input in plaintext
    # If we reduce our input size, flag shifts left into blocks we might control
    
    # Try with minimal input to see raw blocks
    print("[*] Phase 4: Testing different input sizes")
    
    flag_candidates = []
    
    # Try to find repeating blocks that might be part of the flag format
    # "uoftctf{" is the start
    test_prefix = b"uoftctf{"
    
    # Build dictionary for known blocks
    print("[*] Phase 5: Building dictionary attack")
    
    # For each byte position in flag
    flag = bytearray(b"uoftctf{")  # We know this
    
    # Try to find blocks that contain the flag start
    # Strategy: Use input to push known flag prefix into a block, then brute force next byte
    
    for flag_byte_idx in range(len(flag), 60):
        print(f"    Trying to extract flag byte {flag_byte_idx}...")
        
        found_byte = None
        
        # We want to align things so we can brute force
        # Input structure: pl + user_input + FLAG + padding
        # We don't know pl, but it's 0-96 bytes
        
        # Try different alignments
        for pl_guess in range(97):
            # Calculate how much input we need to push flag to block boundary
            # We want: (pl + user_input_len) to align with block boundary
            # Then our flag bytes will be in the next blocks
            
            # Amount to fill to next block boundary after prefix
            to_boundary = (BS - (pl_guess % BS)) % BS
            
            # We want flag[flag_byte_idx] to be at position 15 of some block
            # So we can test with known_flag + guess_byte filling exactly one block
            
            # Input needed: enough to align, then (BS - 1 - len(known_flag))
            known_part = flag[:flag_byte_idx]
            
            # We need input such that: pl + len(input) + flag_byte_idx == k * BS - 1 for some k
            input_len_needed = (BS - 1 - ((pl_guess + flag_byte_idx) % BS)) % BS
            
            if input_len_needed > 256:
                continue
            
            # Build input: filler + known_flag_part
            if len(known_part) <= input_len_needed:
                filler = b'Z' * (input_len_needed - len(known_part))
                test_input = filler + known_part
            else:
                continue
            
            if len(test_input) > 256:
                continue
            
            # Now we query with this input
            reference = query(s, 0, test_input)  # Pick a block index to check
            
            # Try all byte values
            for guess in range(256):
                test_byte = bytes([guess])
                test_input_full = (filler + known_part + test_byte) if len(known_part) <= input_len_needed else None
                
                if test_input_full and len(test_input_full) <= 256:
                    result = query(s, 0, test_input_full[:256])
                    
                    # If this matches a known encrypted block... we need better logic here
        
        # Simplified: just try empty to see patterns
        if not found_byte:
            break
    
    # Let's try a simpler approach - just dump all blocks and analyze
    print("[*] Dumping all blocks with various inputs for manual analysis...")
    
    for input_size in [0, 16, 32, 48, 64, 128, 192, 256]:
        print(f"\n[*] Input size: {input_size}")
        test_input = b'X' * input_size
        blocks = collect_all_blocks(s, test_input)
        
        for idx in range(min(10, n)):
            if idx in blocks:
                print(f"    Block {idx}: {base64.b64encode(blocks[idx]).decode()}")
    
    s.close()
    return None

if __name__ == "__main__":
    find_flag()
