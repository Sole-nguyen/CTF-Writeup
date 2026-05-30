#!/usr/bin/env python3
"""
ORCA Exploit - Reverse the Permutation

The shuffling permutation is FIXED per connection. If we can reverse it,
we can reconstruct the original plaintext blocks before shuffling.

Step 1: Send known plaintext to identify the permutation
Step 2: Query all blocks and unshuffle them
Step 3: Extract flag from reconstructed plaintext blocks
"""

import socket
import base64

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

def reverse_permutation(s):
    """
    Find the inverse permutation by using known repeating blocks.
    
    If we send 16 blocks of 'AAAA...', we know these will all encrypt to the same value.
    By finding which shuffled indices have this same value, we can map the permutation.
    """
    print("[*] Reversing the block permutation...")
    
    # Create 256 bytes of 'A' = 16 blocks of 'AAAA...'
    # After encryption, all these blocks will have the same ciphertext
    test_input = b'A' * 256
    
    # Query all block indices
    blocks = {}
    for idx in range(n):
        enc = query(s, idx, test_input)
        if enc:
            blocks[idx] = enc
    
    # Find the most common encrypted block (this should be our repeated 'A' block)
    from collections import Counter
    block_freq = Counter(blocks.values())
    
    print(f"    Total blocks collected: {len(blocks)}")
    print(f"    Unique encrypted values: {len(set(blocks.values()))}")
    print(f"    Most common blocks:")
    
    for enc_block, count in block_freq.most_common(10):
        print(f"      {base64.b64encode(enc_block).decode()}: {count} times")
    
    # The most frequent block should be our 'AAAA...' block
    most_common_enc, freq = block_freq.most_common(1)[0]
    
    if freq < 10:  # We sent 16 blocks, but some might contain prefix/flag
        print(f"    Warning: Most common block only appears {freq} times")
    
    # Find which indices have this encrypted block
    repeated_indices = [idx for idx, enc in blocks.items() if enc == most_common_enc]
    print(f"    Repeated block at indices: {sorted(repeated_indices)}")
    
    # These indices tell us where blocks from our user input ended up
    # But we don't know the exact mapping yet
    
    # Let's try a different approach: use unique blocks
    print("\n[*] Using unique block patterns to map permutation...")
    
    # Create 16 unique blocks (max we can fit in 256 bytes)
    unique_input = b''.join([bytes([i]) * 16 for i in range(16)])
    
    # For each unique block, we need to identify where it ends up
    # We'll query with input that has one unique block and rest different
    
    permutation_map = {}  # shuffled_index -> original_block_index
    
    # Simplified: Let's just collect all blocks with unique input and analyze
    unique_blocks = {}
    for idx in range(n):
        enc = query(s, idx, unique_input)
        if enc:
            unique_blocks[idx] = enc
    
    print(f"    Collected {len(unique_blocks)} blocks with unique input")
    
    # Show some samples
    for idx in range(min(20, n)):
        if idx in unique_blocks:
            print(f"      Block {idx}: {base64.b64encode(unique_blocks[idx]).decode()}")
    
    return permutation_map, unique_blocks

def extract_flag_direct(s):
    """
    Try a more direct approach: vary input size to control where flag appears.
    """
    print("\n[*] Direct flag extraction attempt...")
    
    # The message structure is: prefix(pl) + input(u) + flag + padding
    # pl is 0-96 bytes (random)
    # We control input up to 256 bytes
    # Flag comes after
    
    # If we use NO input, message is: prefix + flag + padding
    # If we use FULL input (256), message is: prefix + 256_bytes + flag + padding
    
    # Let's collect blocks with different input sizes and look for patterns
    print("[*] Collecting blocks with varying input sizes...")
    
    samples = {}
    for size in [0, 240, 248, 252, 254, 255, 256]:
        test_input = b'X' * size
        blocks = {}
        for idx in range(n):
            enc = query(s, idx, test_input)
            if enc:
                blocks[idx] = enc
        samples[size] = blocks
        print(f"    Size {size}: collected {len(blocks)} blocks")
    
    # Look for blocks that are consistent across certain inputs
    # The flag blocks should appear at different positions as we change input size
    
    print("\n[*] Comparing blocks to find flag position...")
    
    # Compare size 0 vs size 256
    # Blocks that changed contain our input or are affected by alignment
    
    changed_indices = []
    for idx in range(n):
        if idx in samples[0] and idx in samples[256]:
            if samples[0][idx] != samples[256][idx]:
                changed_indices.append(idx)
    
    print(f"    {len(changed_indices)} blocks changed between input size 0 and 256")
    
    # Let's try to find repeating patterns when we use size 256-N where N is small
    # This pushes flag to specific alignment
    
    print("\n[*] Looking for flag pattern...")
    
    # With size 256, our input completely fills the user input space
    # Flag starts right after our controlled 256 bytes
    # If we reduce by 1 byte, flag shifts left by 1 byte
    
    # Let's build a known plaintext: "uoftctf{" and see if we can find it
    flag_prefix = b"uoftctf{"
    
    # Try to find this in the blocks
    # We'll use input of size (256 - len(flag_prefix)) then append flag_prefix
    test = b'A' * (256 - len(flag_prefix)) + flag_prefix
    
    test_blocks = {}
    for idx in range(n):
        enc = query(s, idx, test)
        if enc:
            test_blocks[idx] = enc
    
    print(f"    Collected {len(test_blocks)} blocks with known flag prefix")
    
    # Now try without the flag prefix (just A's)
    ref_test = b'A' * 256
    ref_blocks = {}
    for idx in range(n):
        enc = query(s, idx, ref_test)
        if enc:
            ref_blocks[idx] = enc
    
    # Find blocks that are different
    diff_indices = []
    for idx in range(n):
        if idx in test_blocks and idx in ref_blocks:
            if test_blocks[idx] != ref_blocks[idx]:
                diff_indices.append(idx)
    
    print(f"    {len(diff_indices)} blocks differ when we add flag prefix")
    print(f"    Different indices: {sorted(diff_indices)[:20]}")
    
    # These blocks potentially contain the flag prefix we added
    # But due to shuffling, we need to be more clever
    
    return None

def main():
    print("[*] Connecting to 34.186.247.84:5000")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(30)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    
    try:
        # First, try to understand the permutation
        perm, blocks = reverse_permutation(s)
        
        # Then try direct extraction
        flag = extract_flag_direct(s)
        
        if flag:
            print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")
        else:
            print("\n[-] Need different approach")
            
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        s.close()

if __name__ == "__main__":
    main()
