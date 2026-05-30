#!/usr/bin/env python3
"""
Fast ORCA Exploit

Key insight: We can query individual blocks. If we can identify which blocks
contain the flag and decrypt them, we win.

Approach: Use the fact that AES-ECB is deterministic. Build a dictionary
of known plaintext -> ciphertext, then brute force flag byte-by-byte.
"""

import socket
import base64

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

def fast_extract():
    """
    Fast extraction using minimal queries.
    
    The trick: We know the flag starts with "uoftctf{".
    We'll use this to align our attack.
    """
    s = connect()
    
    print("[*] Attempting fast flag extraction...")
    
    # Collect all blocks with empty input (baseline)
    print("[*] Collecting baseline blocks...")
    baseline = [query(s, i, b"") for i in range(n)]
    
    # Now, let's try to extract by using a sliding window
    # We'll fill input to different lengths and see which blocks contain recognizable patterns
    
    # The flag is somewhere in: prefix + "" + FLAG + padding
    # If we use full input: prefix + 256bytes + FLAG + padding
    
    # Let's use a different strategy: brute force with known prefix
    known_flag = b"uoftctf{"
    
    flag = bytearray(known_flag)
    
    print(f"[*] Starting with: {flag.decode()}")
    
    # For each unknown byte in flag
    for byte_pos in range(len(flag), 60):
        print(f"[*] Extracting byte {byte_pos}...", end='', flush=True)
        
        found = False
        
        # Build dictionary for this position
        # Strategy: Use input to push known flag into a predictable position
        # Then query and match against brute-forced guesses
        
        # We want to align so that: prefix + input + known_flag fills to a block boundary
        # Then we can brute force the next byte
        
        # Try minimal input first
        for input_len in range(0, min(30, 257 - len(flag))):
            # Dictionary: encrypted_block -> guess_byte
            enc_to_guess = {}
            
            padding = b'\x00' * input_len
            
            # Build dictionary by trying all possible next bytes
            for guess in range(256):
                test = padding + flag + bytes([guess])
                
                # Query specific blocks (try a few)
                for check_idx in [5, 10, 15, 20, 25]:  # Sample indices
                    enc = query(s, check_idx, test[:256])
                    if enc and enc not in enc_to_guess:
                        enc_to_guess[enc] = guess
                        break
                
                if len(enc_to_guess) > 250:  # Got most of the dictionary
                    break
            
            # Now query with actual (without guess) and see if we get a match
            actual = padding + flag
            actual = actual + b'\xFF' * (256 - len(actual))  # Pad with distinct byte
            
            for check_idx in [5, 10, 15, 20, 25]:
                enc_actual = query(s, check_idx, actual)
                if enc_actual in enc_to_guess:
                    found_byte = enc_to_guess[enc_actual]
                    flag.append(found_byte)
                    char = chr(found_byte) if 32 <= found_byte < 127 else f'\\x{found_byte:02x}'
                    print(f" {char}")
                    print(f"    Current flag: {flag.decode(errors='ignore')}")
                    found = True
                    break
            
            if found:
                break
        
        if not found:
            print(" failed")
            # Check if we got the closing brace
            if b'}' in flag:
                print("[+] Found complete flag!")
                break
            # Otherwise, try a few more positions
            if byte_pos > 15:
                print("[-] Giving up after multiple failures")
                break
    
    s.close()
    return bytes(flag)

if __name__ == "__main__":
    flag = fast_extract()
    print(f"\n[+] FINAL FLAG: {flag.decode(errors='ignore')}")
