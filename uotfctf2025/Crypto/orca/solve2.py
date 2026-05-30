#!/usr/bin/env python3
"""
ORCA ECB Oracle Exploit

Message structure: random_prefix(pl bytes) + user_input(≤256) + FLAG + random_padding
Total: 1024 bytes before padding, 1040 after PKCS7 = 65 blocks

Attack approach:
Since blocks are shuffled but ECB is deterministic, we can:
1. Query blocks with controlled input to build an encrypted block dictionary  
2. Use the dictionary to identify which blocks contain flag data
3. Reverse the flag by matching encrypted blocks to known plaintexts
"""

import socket
import base64
import sys

BS = 16
n = 65  # Total blocks

def query(s, idx, data=b""):
    """Query oracle and return block at given index"""
    if data:
        req = f"{idx}:{data.hex()}\n"
    else:
        req = f"{idx}\n"
    
    s.sendall(req.encode())
    resp = s.recv(4096).decode()
    
    # Extract just the base64 part (between prompts)
    lines = resp.split('\n')
    for line in lines:
        line = line.strip()
        if line and line != '>' and line != 'error':
            try:
                return base64.b64decode(line)
            except:
                pass
    return None

def build_block_dict(s, known_prefix):
    """
    Build dictionary of encrypted blocks for all possible next bytes.
    Returns dict: encrypted_block -> next_byte
    """
    block_dict = {}
    
    # For each possible byte value
    for b in range(256):
        test_input = known_prefix + bytes([b])
        
        # Pad to fill a complete block if needed
        if len(test_input) % BS != 0:
            test_input += b'A' * (BS - (len(test_input) % BS))
        
        # Ensure we don't exceed max input size
        if len(test_input) > 256:
            continue
        
        # Query a block (we'll try different indices)
        # The tricky part is knowing which block index contains our test data
        for idx in range(n):
            enc_block = query(s, idx, test_input)
            if enc_block and enc_block not in block_dict:
                block_dict[enc_block] = b
                break
    
    return block_dict

def extract_flag_smart(s):
    """
    Extract flag using ECB property.
    
    Key idea: We control input after random prefix.
    If we can align our input properly, we can brute-force flag byte by byte.
    """
    print("[*] Starting smart extraction...")
    
    # First, let's understand the structure by querying with different input sizes
    # and seeing which blocks stay constant vs change
    
    print("[*] Analyzing block structure...")
    
    # Collect blocks with no input
    baseline = {}
    for idx in range(n):
        block = query(s, idx, b"")
        if block:
            baseline[idx] = block
    
    print(f"    Collected {len(baseline)} baseline blocks")
    
    # Collect blocks with full input (256 bytes of 'A')
    full_input = {}
    test = b'A' * 256
    for idx in range(n):
        block = query(s, idx, test)
        if block:
            full_input[idx] = block
    
    # Find which blocks changed
    changed = [i for i in range(n) if baseline.get(i) != full_input.get(i)]
    unchanged = [i for i in range(n) if baseline.get(i) == full_input.get(i)]
    
    print(f"    {len(changed)} blocks changed, {len(unchanged)} stayed same")
    print(f"    Changed indices (first 20): {changed[:20]}")
    print(f"    Unchanged indices (first 20): {unchanged[:20]}")
    
    # The unchanged blocks contain only random padding (after flag)
    # The changed blocks contain our input
    # Some blocks contain the flag
    
    # Try to find flag by looking at blocks when we vary input size
    print("\n[*] Testing input sizes to locate flag...")
    
    for size in [0, 1, 16, 32, 64, 128, 240, 255, 256]:
        print(f"\nInput size {size}:")
        test_input = b'X' * size
        
        for idx in range(min(15, n)):
            block = query(s, idx, test_input)
            if block:
                print(f"  Block {idx}: {base64.b64encode(block).decode()}")
    
    return b""

def main():
    print("[*] Connecting to oracle at 34.186.247.84:5000")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(("34.186.247.84", 5000))
    
    # Read initial prompt
    s.recv(1024)
    
    try:
        flag = extract_flag_smart(s)
        if flag:
            print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
