#!/usr/bin/env python3
"""
Kiss ASIS - Aggressive factoring attempt

Try multiple factorization methods with longer timeouts.
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import time
import random

context.log_level = 'error'

def fermat_factor(n, max_iter=2000000):
    """Fermat factorization"""
    a = isqrt(n) + 1
    for i in range(max_iter):
        b2 = a*a - n
        b = isqrt(b2)
        if b*b == b2:
            return a - b, a + b
        a += 1
        if i % 500000 == 0 and i > 0:
            print(f"    Fermat: {i//1000}k...", end="", flush=True)
    return None, None

def pollard_rho(n, max_iter=2000000):
    """Pollard's rho"""
    if n % 2 == 0:
        return 2, n // 2
    
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    f = lambda x: (x * x + c) % n
    
    for i in range(max_iter):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        if d != 1 and d != n:
            return d, n // d
        if i % 500000 == 0 and i > 0:
            print(f"    Rho: {i//1000}k...", end="", flush=True)
    return None, None

def pollard_p1(n, B=500000):
    """Pollard p-1"""
    a = 2
    for j in range(2, B + 1):
        a = pow(a, j, n)
        if j % 100000 == 0:
            g = gcd(a - 1, n)
            if 1 < g < n:
                return g, n // g
            print(f"    P-1 B={j//1000}k...", end="", flush=True)
    g = gcd(a - 1, n)
    if 1 < g < n:
        return g, n // g
    return None, None

def williams_p1(n, B=100000):
    """Williams p+1"""
    # P+1 attack using Lucas sequences
    for start in range(2, 100):
        V = start
        for j in range(2, B + 1):
            V = (V * V - 2) % n
            if j % 50000 == 0:
                g = gcd(V - 2, n)
                if 1 < g < n:
                    return g, n // g
        g = gcd(V - 2, n)
        if 1 < g < n:
            return g, n // g
    return None, None

def try_all_methods(N, timeout_factor=1.0):
    """Try all factoring methods"""
    print("    Fermat...", end="", flush=True)
    p, q = fermat_factor(N, int(1000000 * timeout_factor))
    if p:
        print(" FOUND!")
        return p, q
    print()
    
    print("    Pollard rho...", end="", flush=True)
    p, q = pollard_rho(N, int(1000000 * timeout_factor))
    if p:
        print(" FOUND!")
        return p, q
    print()
    
    print("    Pollard p-1...", end="", flush=True)
    p, q = pollard_p1(N, int(200000 * timeout_factor))
    if p:
        print(" FOUND!")
        return p, q
    print()
    
    return None, None

def compute_phi(p, q, k):
    """Compute phi_k = (p^k - 1)(q^k - 1)"""
    return (p**k - 1) * (q**k - 1)

def try_decrypt(p, q, N, e, enc):
    """Try to decrypt for all k values"""
    for k in range(1, 7):
        try:
            phi = compute_phi(p, q, k)
            
            # Try both e*d = 1 and e*d = -1 (mod phi)
            for sign in [1, -1]:
                try:
                    d = pow(e * sign, -1, phi)
                    if sign == -1:
                        d = phi - d
                    m = pow(enc, d, N)
                    msg = long_to_bytes(m)
                    
                    # Check if valid printable ASCII
                    if all(32 <= c <= 126 for c in msg) and 10 <= len(msg) <= 50:
                        return msg.decode(), k
                except:
                    pass
        except:
            pass
    return None, None

def try_server():
    """Try one server instance"""
    try:
        io = remote("65.109.214.93", 13137, timeout=30)
        io.recvuntil(b"[Q]uit", timeout=15)
        io.sendline(b"p")
        data = io.recvuntil(b"[Q]uit", timeout=15).decode()
        
        N, e = None, None
        for line in data.split("\n"):
            if "N = " in line: N = int(line.split("N = ")[1].strip())
            if "e = " in line: e = int(line.split("e = ")[1].strip())
        
        if N is None or e is None:
            io.close()
            return False, "Failed to get N, e"
        
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=15).decode()
        
        enc = None
        for line in data.split("\n"):
            if "enc = " in line: enc = int(line.split("enc = ")[1].strip())
        
        if enc is None:
            io.close()
            return False, "Failed to get enc"
        
        n_bits = N.bit_length()
        e_bits = e.bit_length()
        k_estimate = (e_bits + n_bits - 1) // n_bits
        
        print(f"  N: {n_bits} bits, e: {e_bits} bits, k~{k_estimate}")
        
        # Try factoring
        p, q = try_all_methods(N, timeout_factor=1.0)
        
        if p is not None:
            print(f"  Factored! p: {p.bit_length()} bits")
            
            msg, k = try_decrypt(p, q, N, e, enc)
            
            if msg:
                print(f"  Decrypted (k={k}): {msg}")
                
                io.sendline(b"s")
                io.recvuntil(b"secret message:", timeout=10)
                io.sendline(msg.encode())
                response = io.recvall(timeout=10).decode()
                print(f"  Response: {response}")
                io.close()
                return True, response
        
        io.close()
        return False, "Could not factor"
    
    except Exception as ex:
        return False, str(ex)

def main():
    print("="*60)
    print("Kiss ASIS - Aggressive Factoring")
    print("="*60)
    
    for attempt in range(30):
        print(f"\nAttempt {attempt + 1}...")
        
        success, result = try_server()
        
        if success:
            print("\n" + "="*60)
            print("SUCCESS!")
            print(result)
            print("="*60)
            break
        else:
            print(f"  Result: {result[:50]}..." if len(result) > 50 else f"  Result: {result}")
        
        time.sleep(1)
    
    print("\nDone")

if __name__ == "__main__":
    main()
