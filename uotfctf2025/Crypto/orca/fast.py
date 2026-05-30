#!/usr/bin/env python3
"""
Ultra-fast ORCA exploit - parallel queries
"""
import socket, base64, threading, queue

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

def exploit_fast():
    s = socket.socket()
    s.settimeout(30)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    
    print("[*] Fast oracle attack...")
    
    # Use block 1 (from previous test, it's controllable)
    blk = 1
    
    flag = bytearray(b"uoftctf{")
    print(f"Starting: {flag.decode()}")
    
    # For each byte
    for pos in range(len(flag), 45):
        print(f"Byte {pos}... ", end='', flush=True)
        
        found = False
        
        # Try a few input sizes
        for pad_len in [0, 15, 31]:
            if found: break
            
            pad = b'P' * pad_len
            
            # Build lookup dict (parallel would be ideal, but let's keep it simple for now)
            d = {}
            
            # Only try printable characters + common flag chars first
            charset = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'
            
            for g in charset:
                test = (pad + flag + bytes([g]))[:256]
                enc = q(s, blk, test)
                if enc and enc not in d:
                    d[enc] = g
            
            # Query actual
            actual = (pad + flag + b'Q' * max(0, 256 - pad_len - len(flag)))[:256]
            enc_actual = q(s, blk, actual)
            
            if enc_actual in d:
                byte_val = d[enc_actual]
                flag.append(byte_val)
                print(f"{chr(byte_val)}")
                print(f"   -> {flag[8:].decode(errors='ignore')}")
                found = True
                break
        
        if not found:
            # Try full charset
            for pad_len in [0]:
                if found: break
                pad = b'P' * pad_len
                d = {}
                
                for g in range(256):
                    test = (pad + flag + bytes([g]))[:256]
                    enc = q(s, blk, test)
                    if enc and enc not in d:
                        d[enc] = g
                
                actual = (pad + flag + b'Q' * max(0, 256 - pad_len - len(flag)))[:256]
                enc_actual = q(s, blk, actual)
                
                if enc_actual in d:
                    byte_val = d[enc_actual]
                    flag.append(byte_val)
                    print(f"\\x{byte_val:02x}")
                    found = True
                    break
        
        if not found:
            print("FAIL")
        
        if b'}' in flag[8:]:  # Check if we hit closing brace
            print("\nFound closing brace!")
            break
    
    s.close()
    result = flag.decode(errors='ignore')
    print(f"\n[+] FLAG: {result}")
    return result

exploit_fast()
