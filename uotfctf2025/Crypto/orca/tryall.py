#!/usr/bin/env python3
"""
ORCA - Try all blocks approach
"""
import socket, base64

def q(s, idx, data=b""):
    try:
        s.sendall(f"{idx}:{data.hex()}\n".encode() if data else f"{idx}\n".encode())
        r = s.recv(4096).decode()
        for l in r.split('\n'):
            l = l.strip()
            if l and l not in ['>', 'error']:
                try: return base64.b64decode(l)
                except: pass
    except:
        pass
    return None

s = socket.socket()
s.settimeout(20)
s.connect(("34.186.247.84", 5000))
s.recv(1024)

print("[*] Extracting flag - trying all blocks...")

flag = bytearray(b"uoftctf{")
print(f"Start: {flag.decode()}")

for pos in range(len(flag), 40):
    print(f"\n[*] Byte {pos}:", flush=True)
    found = False
    
    # Try all blocks and all pad lengths
    for blk in range(0, 65, 5):  # Try every 5th block
        if found: break
        
        for pad_len in [0, 7, 15]:
            if found: break
            
            pad = b'Z' * pad_len
            
            # Small charset first
            d = {}
            for c in b'abcdefghijklmnopqrstuvwxyz0123456789_{}':
                test = (pad + flag + bytes([c]))[:256]
                enc = q(s, blk, test)
                if enc and enc not in d:
                    d[enc] = c
            
            # Query actual
            actual = (pad + flag)
            actual += b'W' * max(0, 256 - len(actual))
            enc_act = q(s, blk, actual[:256])
            
            if enc_act in d:
                b_val = d[enc_act]
                flag.append(b_val)
                print(f"  Found: {chr(b_val)} (block={blk}, pad={pad_len})")
                print(f"  Flag: uoftctf{{{flag[8:].decode()}}}")
                found = True
                break
    
    if not found:
        print("  FAIL - trying next position anyway")
    
    if b'}' in flag[8:]:
        break

s.close()
print(f"\n[+] FINAL: {flag.decode(errors='ignore')}")
