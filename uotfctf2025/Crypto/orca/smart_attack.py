#!/usr/bin/env python3
"""
Final working exploit based on collected data.

Key findings:
- Block 6 is invariant (always "08wA9VIC875JTh5B+P/JdQ==") - it's pure random padding
- Blocks [2, 14, 19, 24, 26, 27, 28, 35, 37, 38, 44, 54, 55, 56, 64] contain our repeated 'A' pattern
- This means we control these block positions (after accounting for prefix and boundaries)

Strategy: Use blocks that are NOT in the invariant/repeated sets to extract the flag.
These blocks likely contain prefix + flag data.
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
    
    print("[*] Smart flag extraction...")
    
    # Blocks that are controlled by our 'A' input
    controlled_by_A = [2, 14, 19, 24, 26, 27, 28, 35, 37, 38, 44, 54, 55, 56, 64]
    
    # Block that's invariant (pure padding)
    invariant = [6]
    
    # Other blocks likely contain prefix + flag
    potential_flag_blocks = [i for i in range(65) if i not in controlled_by_A and i not in invariant]
    
    print(f"    Potential flag block indices: {potential_flag_blocks[:15]}...")
    
    # Byte-by-byte extraction using these specific blocks
    flag = bytearray(b"uoftctf{")
    
    for pos in range(len(flag), 50):
        print(f"  Position {pos}: ", end='', flush=True)
        
        found = False
        
        # Try each potential flag block
        for blk_idx in potential_flag_blocks[:10]:  # Try first 10
            if found: break
            
            # Try different padding lengths
            for pad_len in range(16):
                if found: break
                
                # Build dictionary for this byte
                d = {}
                padding = b'\x00' * pad_len
                
                for guess in range(256):
                    test_input = padding + flag + bytes([guess])
                    test_input = test_input[:256]  # Truncate to max
                    
                    enc = q(s, blk_idx, test_input)
                    if enc and enc not in d:
                        d[enc] = guess
                
                # Query with actual (no guess byte)
                actual_input = padding + flag
                # Pad to a different value so it's distinct
                actual_input = actual_input + b'\xFF' * max(0, 256 - len(actual_input))
                actual_input = actual_input[:256]
                
                enc_actual = q(s, blk_idx, actual_input)
                
                if enc_actual in d:
                    byte_val = d[enc_actual]
                    flag.append(byte_val)
                    ch = chr(byte_val) if 32 <= byte_val < 127 else f'\\x{byte_val:02x}'
                    print(f"{ch}")
                    print(f"      Current: {flag[8:].decode(errors='ignore')}")
                    found = True
                    break
        
        if not found:
            print("X")
            if b'}' in flag:
                print("\n[+] Found closing brace!")
                break
            if pos > 20:
                print("\n[-] Too many failures, stopping")
                break
    
    s.close()
    print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")
    return flag

exploit()
