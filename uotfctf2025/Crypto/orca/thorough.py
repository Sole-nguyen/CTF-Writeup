#!/usr/bin/env python3
"""
ORCA - More thorough search
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
    except Exception as e:
        print(f"Query error: {e}", file=sys.stderr)
    return None

s = socket.socket()
s.settimeout(20)
s.connect(("34.186.247.84", 5000))
s.recv(1024)

print("[*] Extracting with thorough search...")

flag = bytearray(b"uoftctf{")
print(f"Start: {flag.decode()}")

for pos in range(len(flag), 50):
    print(f"\nByte {pos}:", flush=True)
    found = False
    
    # Try more blocks and more padding values
    for blk in range(65):  # Try ALL blocks
        if found: break
        
        for pad_len in range(16):  # Try ALL alignments
            if found: break
            
            pad = b'Z' * pad_len
            
            # Build dictionary
            d = {}
            charset = b'abcdefghijklmnopqrstuvwxyz0123456789_{}'
            
            for c in charset:
                test = (pad + flag + bytes([c]))[:256]
                enc = q(s, blk, test)
                if enc and enc not in d:
                    d[enc] = c
            
            # Query actual
            actual = pad + flag
            actual += b'W' * max(0, 256 - len(actual))
            enc_act = q(s, blk, actual[:256])
            
            if enc_act in d:
                b_val = d[enc_act]
                flag.append(b_val)
                print(f"  -> {chr(b_val)} (blk={blk}, pad={pad_len})")
                print(f"  Flag so far: {flag.decode()}")
                found = True
                break
        
        # Progress indicator
        if blk % 10 == 0 and not found:
            print(f"  ...checked {blk} blocks", flush=True)
    
    if not found:
        print("  X - Not found, stopping")
        break
    
    if b'}' in flag[8:]:
        print("\n[+] Found closing brace!")
        break

s.close()
print(f"\n[+] FINAL FLAG: {flag.decode(errors='ignore')}")
