#!/usr/bin/env python3
"""
Collect data once, analyze offline
"""
import socket, base64, pickle

def q(s, idx, data=b""):
    s.sendall(f"{idx}:{data.hex()}\n".encode() if data else f"{idx}\n".encode())
    r = s.recv(4096).decode()
    for l in r.split('\n'):
        l = l.strip()
        if l and l not in ['>', 'error']:
            try: return base64.b64decode(l)
            except: pass
    return None

def collect():
    s = socket.socket()
    s.settimeout(10)
    s.connect(("34.186.247.84", 5000))
    s.recv(1024)
    
    print("[*] Collecting data...")
    
    data = {}
    
    # Collect with various inputs
    for input_type in ["empty", "A", "B", "uoftctf{"]:
        print(f"  Collecting with input: {input_type}")
        
        if input_type == "empty":
            test = b""
        elif input_type == "A":
            test = b"A" * 256
        elif input_type == "B":
            test = b"B" * 256
        else:
            test = input_type.encode() * 32  # Repeat to fill
            test = test[:256]
        
        blocks = {}
        for idx in range(65):
            enc = q(s, idx, test)
            if enc:
                blocks[idx] = enc
        
        data[input_type] = blocks
        print(f"    Collected {len(blocks)} blocks")
    
    s.close()
    
    # Save data
    with open("oracle_data.pkl", "wb") as f:
        pickle.dump(data, f)
    
    print("[*] Data saved to oracle_data.pkl")
    print("\n[*] Analysis:")
    
    # Compare blocks
    for i in range(10):
        print(f"\nBlock {i}:")
        for inp in ["empty", "A", "B", "uoftctf{"]:
            if i in data[inp]:
                print(f"  {inp:12s}: {base64.b64encode(data[inp][i]).decode()}")
    
    # Look for patterns
    print("\n[*] Looking for repeated blocks...")
    for inp in ["A", "B"]:
        from collections import Counter
        c = Counter(data[inp].values())
        print(f"\n  Input '{inp}':")
        for enc, count in c.most_common(5):
            if count > 1:
                indices = [i for i, e in data[inp].items() if e == enc]
                print(f"    {base64.b64encode(enc).decode()}: {count}x at {indices}")

collect()
