#!/usr/bin/env python3
"""
Efficient ORCA exploit - comparison-based extraction

Instead of building full dictionaries, we use binary search or direct comparison.
Key idea: If we can find a block index that consistently responds to our input in a predictable way,
we can extract flag byte-by-byte with minimal queries.
"""

import socket, base64

def q(s, idx, data=b""):
    s.sendall(f"{idx}:{data.hex()}\n".encode() if data else f"{idx}\n".encode())
    r = s.recv(4096).decode()
    for l in r.split('\n'):
        l = l.strip()
        if l and l not in ['>', 'error']:
            try: return base64.b64decode(l)
            except: pass
    return None

def exploit():
    s = socket.socket()
    s.settimeout(10)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    
    print("[*] Efficient flag extraction using ECB oracle...")
    
    # Find a block that we can reliably control
    # Test which block index gives us repeatable results
    print("[*] Finding controllable block...")
    
    test_idx = None
    for idx in range(30):  # Test first 30 blocks
        # Send two different inputs and see if we get different outputs
        enc_A = q(s, idx, b"A" * 256)
        enc_B = q(s, idx, b"B" * 256)
        
        if enc_A != enc_B:
            # This block responds to our input
            # Verify it's consistent with same input
            enc_A2 = q(s, idx, b"A" * 256)
            if enc_A == enc_A2:  # Same input = same output (ECB property)
                # Consistent! We can use this block
                test_idx = idx
                print(f"    Found controllable block at index {idx}")
                break
    
    # If we didn't find one in first 30, just use block 0
    if test_idx is None:
        test_idx = 0
        print(f"    Using default block index {test_idx}")
    
    if test_idx is None:
        print("[-] Could not find controllable block")
        test_idx = 0  # Just try with block 0
        print(f"    Using default block {test_idx}")
    
    # Now extract flag byte-by-byte
    flag = bytearray(b"uoftctf{")
    print(f"[*] Starting extraction from: {flag.decode()}")
    
    for pos in range(len(flag), 50):
        print(f"  Byte {pos}: ", end='', flush=True)
        
        found = False
        
        # Try to align the flag so we can brute force the next byte
        # We'll try different input sizes to find one that works
        
        for input_size in range(256 - len(flag) + 1):
            if found: break
            
            # Padding before flag
            pad = b'X' * input_size
            
            # Try all possible next bytes
            candidates = {}
            
            # Sample a few guesses to build a small dictionary
            for guess in [ord('a'), ord('z'), ord('0'), ord('9'), ord('}'), ord('_'), ord('{')]:
                test = pad + flag + bytes([guess])
                if len(test) <= 256:
                    enc = q(s, test_idx, test)
                    if enc:
                        candidates[enc] = guess
            
            # Now query with the actual flag (no guess)
            actual = pad + flag
            if len(actual) < 256:
                actual += b'Z' * (256 - len(actual))
            
            enc_actual = q(s, test_idx, actual[:256])
            
            if enc_actual in candidates:
                # We got a match! But it might be wrong, let's verify by trying all
                likely_byte = candidates[enc_actual]
                
                # Full brute force for this alignment
                full_dict = {}
                for g in range(256):
                    test = pad + flag + bytes([g])
                    if len(test) <= 256:
                        enc = q(s, test_idx, test)
                        if enc and enc not in full_dict:
                            full_dict[enc] = g
                
                if enc_actual in full_dict:
                    byte_val = full_dict[enc_actual]
                    flag.append(byte_val)
                    ch = chr(byte_val) if 32 <= byte_val < 127 else f'?'
                    print(f"{ch} ({hex(byte_val)})")
                    print(f"      Flag: uoftctf{{{flag[8:].decode(errors='ignore')}}}")
                    found = True
                    break
        
        if not found:
            print("FAIL")
            if b'}' in flag:
                break
            if pos > 25:
                break
    
    s.close()
    final = flag.decode(errors='ignore')
    print(f"\n[+] FINAL FLAG: {final}")
    return final

exploit()
