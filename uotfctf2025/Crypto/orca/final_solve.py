#!/usr/bin/env python3
"""
ORCA - Final adaptive exploit

The key insight: We need to find working (block, pad) parameters for THIS specific connection,
then use them to extract the entire flag.
"""
import socket, base64, sys

def q(s, idx, data=b""):
    try:
        s.sendall(f"{idx}:{data.hex()}\n".encode() if data else f"{idx}\n".encode())
        r = s.recv(4096).decode()
        for l in r.split('\n'):
            l = l.strip()
            if l and l not in ['>', 'error']:
                try:
                    return base64.b64decode(l)
                except:
                    pass
    except:
        pass
    return None

print("[*] Connecting...")
s = socket.socket()
s.settimeout(15)
s.connect(("34.186.247.84", 5000))
s.recv(1024)

print("[*] Finding working parameters...")

# Find parameters that work for extracting the FIRST byte after "uoftctf{"
# We know the flag starts with "uoftctf{", so test against that

flag_start = b"uoftctf{"
test_byte = None
work_blk, work_pad = None, None

# Try to find params that let us distinguish between different byte values
for pad_len in range(16):  # Try all pad lengths
    if work_blk is not None:
        break
    
    for blk in range(65):  # Try all blocks
        if work_blk is not None:
            break
        
        pad = b'Z' * pad_len
        
        # Test: can we distinguish 'a' from 'b' at position after "uoftctf{"?
        # Use exactly the approach we'll use for real extraction
        test_input_a = (pad + flag_start + b'a')[:256]
        test_input_a = test_input_a + b'W' * max(0, 256 - len(test_input_a))
        
        test_input_b = (pad + flag_start + b'b')[:256]
        test_input_b = test_input_b + b'W' * max(0, 256 - len(test_input_b))
        
        enc_a = q(s, blk, test_input_a)
        enc_b = q(s, blk, test_input_b)
        
        if enc_a and enc_b and enc_a != enc_b:
            # Verify: Build dict and check if we can recover 'a'
            d = {}
            for c in b'abcdefghijklmnopqrstuvwxyz':
                test = (pad + flag_start + bytes([c]))[:256]
                test = test + b'W' * max(0, 256 - len(test))
                enc = q(s, blk, test)
                if enc and enc not in d:
                    d[enc] = c
            
            # Now check if 'a' maps correctly
            if enc_a in d and d[enc_a] == ord('a'):
                work_blk, work_pad = blk, pad_len
                print(f"[+] Found working parameters: block={blk}, pad={pad_len}")
                print(f"    Verified with test characters")
                break

if work_blk is None:
    print("[-] Could not find working parameters")
    s.close()
    sys.exit(1)

# Now extract the flag using these parameters
print(f"[*] Extracting flag...")

flag = bytearray(flag_start)
print(f"Start: {flag.decode()}\n")

for pos in range(len(flag), 50):
    print(f"Byte {pos}: ", end='', flush=True)
    
    pad = b'Z' * work_pad
    
    # Build dictionary with common characters
    d = {}
    charset = b'abcdefghijklmnopqrstuvwxyz0123456789_{} !@#$%^&*()-=+[]|;:,.<>?/'
    
    for c in charset:
        test = (pad + flag + bytes([c]))[:256]
        enc = q(s, work_blk, test)
        if enc and enc not in d:
            d[enc] = c
    
    # Query actual
    actual = pad + flag
    actual += b'W' * max(0, 256 - len(actual))
    enc_act = q(s, work_blk, actual[:256])
    
    if enc_act in d:
        b_val = d[enc_act]
        flag.append(b_val)
        ch = chr(b_val) if 32 <= b_val < 127 else f'\\x{b_val:02x}'
        print(f"{ch} -> {flag[8:].decode(errors='ignore')}")
    else:
        print("X")
        break  # Stop if we can't find the byte
    
    if b'}' in flag[8:]:
        print("\n[+] Found closing brace!")
        break

s.close()
final_flag = flag.decode(errors='ignore')
print(f"\n[+] FINAL FLAG: {final_flag}")
print(f"\n{final_flag}")  # Print just the flag on its own line
