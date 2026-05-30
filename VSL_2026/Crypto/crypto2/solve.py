#!/usr/bin/env python3
import socket
from Crypto.Util.number import long_to_bytes
from sympy import factorint

def interact_with_server(host, port, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    # Read initial prompt
    data = s.recv(1024).decode()
    print(f"Server: {data}")
    
    # Send size
    s.send(f"{size}\n".encode())
    
    # Receive response
    response = s.recv(4096).decode()
    print(f"Response: {response}")
    
    s.close()
    return response

def parse_response(response):
    lines = response.strip().split('\n')
    results = []
    for i in range(0, len(lines), 3):
        if i+2 < len(lines):
            line1 = int(lines[i])
            line2 = int(lines[i+1])
            parts = lines[i+2].split()
            if len(parts) == 3:
                c = int(parts[0])
                e = int(parts[1])
                n = int(parts[2])
                results.append((line1, line2, c, e, n))
    return results

# Collect multiple responses to find pattern
host = "124.197.22.141"
port = 6665

print("Collecting samples...")
for size in [100, 100, 100]:
    response = interact_with_server(host, port, size)
    data = parse_response(response)
    
    for item in data:
        line1, line2, c, e, n = item
        print(f"\nFirst number: {line1}")
        print(f"Second number: {line2}")
        print(f"c: {c}")
        print(f"e: {e}")
        print(f"n: {n}")
        print(f"n bit length: {n.bit_length()}")
        
        # Try to factor small N
        if n.bit_length() <= 100:
            print("Trying to factor N...")
            factors = factorint(n)
            print(f"Factors: {factors}")
            
            if len(factors) == 2:
                p, q = list(factors.keys())
                phi = (p-1)*(q-1)
                d = pow(e, -1, phi)
                m = pow(c, d, n)
                print(f"Decrypted: {m}")
                print(f"As bytes: {long_to_bytes(m)}")
