#!/usr/bin/env python3
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

def solve():
    s = socket.socket()
    s.settimeout(15)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    
    print("[*] Brute forcing flag byte-by-byte...")
    flag = bytearray(b"uoftctf{")
    
    for pos in range(len(flag), 60):
        print(f"Position {pos}: ", end='', flush=True)
        
        # Try different block indices and input alignments
        found = False
        for blk_idx in range(10, 30):  # Try different block positions
            if found: break
            
            for align in range(16):  # Try different alignments
                if found: break
                
                # Build dictionary
                d = {}
                pad = b'A' * align
                
                for g in range(256):
                    t = (pad + flag + bytes([g]))[:256]
                    e = q(s, blk_idx, t)
                    if e and e not in d:
                        d[e] = g
                
                # Query with actual
                actual = (pad + flag)[:256] + b'B' * max(0, 256 - len(pad) - len(flag))
                e_actual = q(s, blk_idx, actual)
                
                if e_actual in d:
                    b = d[e_actual]
                    flag.append(b)
                    print(f"{chr(b) if 32 <= b < 127 else '?'} -> {flag[8:].decode(errors='ignore')}")
                    found = True
                    break
        
        if not found:
            print("X")
            if b'}' in flag or pos > 20:
                break
    
    s.close()
    print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")

solve()
