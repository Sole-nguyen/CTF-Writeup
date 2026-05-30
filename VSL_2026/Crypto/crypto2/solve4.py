#!/usr/bin/env python3
import socket
from Crypto.Util.number import long_to_bytes
from sympy import factorint, isprime

def get_data(host, port, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    s.recv(1024)
    s.send(f"{size}\n".encode())
    
    response = s.recv(4096).decode()
    s.close()
    
    lines = response.strip().split('\n')
    if len(lines) >= 3:
        num1 = int(lines[0])
        num2 = int(lines[1])
        parts = lines[2].split()
        if len(parts) == 3:
            c = int(parts[0])
            e = int(parts[1])
            n = int(parts[2])
            return num1, num2, c, e, n
    return None

host = "124.197.22.141"
port = 6665

# Get a sample
num1, num2, c, e, n = get_data(host, port, 100)

print(f"num1: {num1}")
print(f"num2: {num2}")
print(f"c: {c}")
print(f"e: {e}")
print(f"n: {n}")
print(f"n bit length: {n.bit_length()}")

# Check if num1 and num2 are primes
print(f"\nnum1 is prime: {isprime(num1)}")
print(f"num2 is prime: {isprime(num2)}")

# Check if num1 * num2 == n
print(f"\nnum1 * num2 = {num1 * num2}")
print(f"Does num1 * num2 == n? {num1 * num2 == n}")

# If so, we have p and q!
if num1 * num2 == n:
    p, q = num1, num2
    phi = (p - 1) * (q - 1)
    
    # But c is 0, so there's no message encrypted
    # Maybe the flag is in a different format?
    
    # Let's try getting multiple samples and see if there's a pattern
    print("\n\nCollecting multiple samples...")
    flag_chars = []
    
    for i in range(50):
        data = get_data(host, port, 100)
        if data:
            n1, n2, c, e, n = data
            # The character might be derived from p or q somehow
            # Try p mod 256
            char_code = n2 % 256
            if 32 <= char_code <= 126:
                flag_chars.append(chr(char_code))
                print(chr(char_code), end='', flush=True)
    
    print(f"\n\nFlag attempt: {''.join(flag_chars)}")
