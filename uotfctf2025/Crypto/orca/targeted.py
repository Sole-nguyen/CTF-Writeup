#!/usr/bin/env python3
"""
ORCA - Use parameters from successful run: block=20, pad=15
"""
import socket, base64

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

s = socket.socket()
s.settimeout(15)
s.connect(("34.186.247.84", 5000))
s.recv(1024)

print("[*] Using optimal parameters from previous run")

# Parameters that worked before
blk = 20
pad_len = 15

flag = bytearray(b"uoftctf{")
print(f"Start: {flag.decode()}\n")

for pos in range(len(flag), 45):
    print(f"Byte {pos}: ", end='', flush=True)
    
    pad = b'Z' * pad_len
    
    # Build dictionary
    d = {}
    charset = b'abcdefghijklmnopqrstuvwxyz0123456789_{} '
    
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
        ch = chr(b_val) if 32 <= b_val < 127 else f'\\x{b_val:02x}'
        print(f"{ch}")
    else:
        print("X")
        # Try to continue anyway
    
    print(f"  Current: {flag[8:].decode(errors='ignore')}\n")
    
    if b'}' in flag[8:]:
        print("[+] Found closing brace!")
        break

s.close()
print(f"\n[+] FINAL FLAG: {flag.decode(errors='ignore')}")
