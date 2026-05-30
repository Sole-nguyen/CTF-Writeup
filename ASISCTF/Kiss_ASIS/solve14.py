#!/usr/bin/env python3
"""
Kiss ASIS - Multi-attempt solver
Try multiple connections hoping for weak parameters
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import time

context.log_level = 'error'

def try_factor(N, max_iter=500000):
    """Try various factoring methods"""
    
    # Fermat factorization
    a = isqrt(N) + 1
    for i in range(min(100000, max_iter)):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            p = a - b
            q = a + b
            if p * q == N and p > 1 and q > 1:
                return p, q
        a += 1
    
    # Pollard rho
    x, y, d = 2, 2, 1
    f = lambda x: (x*x + 1) % N
    for i in range(max_iter):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x-y), N)
        if d != 1 and d != N:
            return d, N // d
    
    # Pollard p-1
    a = 2
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
        for _ in range(100):
            a = pow(a, p, N)
        g = gcd(a - 1, N)
        if 1 < g < N:
            return g, N // g
    
    return None, None

def decrypt(p, q, N, e, enc):
    """Try to decrypt with all k values"""
    for k in range(1, 7):
        try:
            phi = (p**k - 1) * (q**k - 1)
            d = pow(e, -1, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            if all(32 <= c <= 126 for c in msg) and len(msg) >= 14:
                return msg.decode(), k
        except:
            pass
    return None, None

def try_server():
    """Try to solve one server instance"""
    try:
        io = remote("65.109.214.93", 13137, timeout=15)
        
        # Get parameters
        io.recvuntil(b"[Q]uit", timeout=5)
        io.sendline(b"p")
        
        data = io.recvuntil(b"[Q]uit", timeout=5).decode()
        
        N = None
        e = None
        for line in data.split("\n"):
            if "N = " in line:
                N = int(line.split("N = ")[1].strip())
            if "e = " in line:
                e = int(line.split("e = ")[1].strip())
        
        if N is None or e is None:
            io.close()
            return False
        
        # Get encrypted message
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=5).decode()
        
        enc = None
        for line in data.split("\n"):
            if "enc = " in line:
                enc = int(line.split("enc = ")[1].strip())
        
        if enc is None:
            io.close()
            return False
        
        print(f"\nGot parameters:")
        print(f"  N bits: {N.bit_length()}")
        print(f"  e bits: {e.bit_length()}")
        
        # Quick analysis
        ratio = e.bit_length() - N.bit_length()
        print(f"  e_bits - N_bits = {ratio} (suggests k ~ {ratio // N.bit_length() + 1})")
        
        # Try to factor
        print("  Trying to factor...")
        p, q = try_factor(N, 100000)
        
        if p is not None:
            print(f"  Found factors!")
            print(f"  p = {p}")
            print(f"  q = {q}")
            
            msg, k = decrypt(p, q, N, e, enc)
            if msg:
                print(f"  Decrypted (k={k}): {msg}")
                
                # Send to server
                io.sendline(b"s")
                io.recvuntil(b"secret message:", timeout=5)
                io.sendline(msg.encode())
                response = io.recvall(timeout=5).decode()
                print(f"  Server response: {response}")
                
                if "flag" in response.lower():
                    io.close()
                    return True
        
        io.close()
        return False
    
    except Exception as ex:
        print(f"  Error: {ex}")
        return False

def main():
    print("="*60)
    print("Kiss ASIS - Multi-attempt solver")
    print("="*60)
    
    attempts = 0
    while attempts < 50:
        attempts += 1
        print(f"\nAttempt {attempts}...")
        
        if try_server():
            print("\n" + "="*60)
            print("SUCCESS!")
            print("="*60)
            break
        
        time.sleep(1)  # Rate limiting
    
    print(f"\nTotal attempts: {attempts}")

if __name__ == "__main__":
    main()
