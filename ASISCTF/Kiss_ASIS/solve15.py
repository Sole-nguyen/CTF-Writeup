#!/usr/bin/env python3
"""
Kiss ASIS - Specialized solver for k=1 case

When k=1 and e ~ N (small e), Wiener attack might work!

For k=1: phi = (p-1)(q-1) = N - p - q + 1
e*d = 1 (mod phi) or e*d = -1 (mod phi)

Wiener attack works when d < N^(1/4) / 3
Here d ~ N, so standard Wiener doesn't work.

But if e ~ N (not e ~ N^2), the relationship changes.
e*d ~ N^2 and phi ~ N, so t = (e*d)/phi ~ N.

Hmm, still large t.

But wait - for k=1 with e ~ N:
e / phi ~ e / N ~ 1 (since e ~ N)
And e*d = t*phi + eps
So t ~ e*d / phi ~ N*N/N = N

Actually, for k=1 case, let me try continued fractions differently.
Since e*d = t*phi + eps and phi = N + 1 - (p+q):
e*d = t*(N + 1 - s) + eps where s = p + q

e/N ~ t*(1 + 1/N - s/N) / d ~ t/d * (1 - s/N)

Since s ~ 2*sqrt(N), s/N ~ 2/sqrt(N) is small.
So e/N ~ t/d approximately.

For Wiener to work on e/N, we need t/d to have small convergent.
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import time

context.log_level = 'error'

def continued_fraction(num, den, limit=500):
    """Get continued fraction coefficients"""
    cf = []
    while den != 0 and len(cf) < limit:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf

def convergents(cf):
    """Get convergents from continued fraction"""
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    for a in cf:
        h2 = a * h1 + h0
        k2 = a * k1 + k0
        yield (h2, k2)
        h0, h1 = h1, h2
        k0, k1 = k1, k2

def try_wiener_k1(N, e, enc):
    """Try Wiener-like attack for k=1"""
    print("    Trying Wiener on e/N for k=1...")
    
    cf = continued_fraction(e, N, 500)
    
    for t_cand, d_cand in convergents(cf):
        if d_cand == 0 or t_cand == 0:
            continue
        
        for eps in [1, -1]:
            val = e * d_cand - eps
            if val <= 0:
                continue
            if val % t_cand != 0:
                continue
            
            phi = val // t_cand
            if phi <= 0:
                continue
            
            # For k=1: phi = N + 1 - s where s = p + q
            s = N + 1 - phi
            if s <= 0:
                continue
            
            disc = s*s - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (s + sqrt_disc) // 2
            q = (s - sqrt_disc) // 2
            
            if p > 1 and q > 1 and p * q == N:
                print(f"    Found! t={t_cand}, d={d_cand}")
                return p, q
    
    return None, None

def try_wiener_k2(N, e, enc):
    """Try Wiener-like attack for k=2"""
    print("    Trying Wiener on e/N^2 for k=2...")
    
    N2 = N * N
    cf = continued_fraction(e, N2, 500)
    
    for t_cand, d_cand in convergents(cf):
        if d_cand == 0 or t_cand == 0:
            continue
        
        for eps in [1, -1]:
            val = e * d_cand - eps
            if val <= 0:
                continue
            if val % t_cand != 0:
                continue
            
            phi = val // t_cand
            if phi <= 0:
                continue
            
            # For k=2: phi = (N+1)^2 - s^2 where s = p + q
            s_sq = (N+1)**2 - phi
            if s_sq <= 0:
                continue
            s = isqrt(s_sq)
            if s*s != s_sq:
                continue
            
            disc = s*s - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (s + sqrt_disc) // 2
            q = (s - sqrt_disc) // 2
            
            if p > 1 and q > 1 and p * q == N:
                print(f"    Found! t={t_cand}, d={d_cand}")
                return p, q
    
    return None, None

def try_factor_quick(N, max_iter=50000):
    """Quick factoring attempts"""
    
    # Fermat
    a = isqrt(N) + 1
    for i in range(min(10000, max_iter)):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            p, q = a - b, a + b
            if p * q == N and p > 1:
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
    
    return None, None

def decrypt(p, q, N, e, enc):
    """Try to decrypt with all k values"""
    for k in range(1, 7):
        try:
            phi = (p**k - 1) * (q**k - 1)
            d = pow(e, -1, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            if all(32 <= c <= 126 for c in msg) and 14 <= len(msg) <= 40:
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
        
        N, e = None, None
        for line in data.split("\n"):
            if "N = " in line:
                N = int(line.split("N = ")[1].strip())
            if "e = " in line:
                e = int(line.split("e = ")[1].strip())
        
        if N is None or e is None:
            io.close()
            return False, None
        
        # Get encrypted message
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=5).decode()
        
        enc = None
        for line in data.split("\n"):
            if "enc = " in line:
                enc = int(line.split("enc = ")[1].strip())
        
        if enc is None:
            io.close()
            return False, None
        
        n_bits = N.bit_length()
        e_bits = e.bit_length()
        
        print(f"  N bits: {n_bits}, e bits: {e_bits}")
        
        p, q = None, None
        
        # Determine likely k and try appropriate attack
        if e_bits <= n_bits + 100:  # e ~ N, likely k=1
            print("    Likely k=1")
            p, q = try_wiener_k1(N, e, enc)
        elif e_bits <= 2 * n_bits + 100:  # e ~ N^2, likely k=2
            print("    Likely k=2")
            p, q = try_wiener_k2(N, e, enc)
        
        # Always try quick factoring
        if p is None:
            print("    Trying quick factor...")
            p, q = try_factor_quick(N)
        
        if p is not None:
            print(f"  Found factors!")
            msg, k = decrypt(p, q, N, e, enc)
            if msg:
                print(f"  Decrypted (k={k}): {msg}")
                
                io.sendline(b"s")
                io.recvuntil(b"secret message:", timeout=5)
                io.sendline(msg.encode())
                response = io.recvall(timeout=5).decode()
                print(f"  Response: {response}")
                
                io.close()
                return "flag" in response.lower(), response
        
        io.close()
        return False, None
    
    except Exception as ex:
        print(f"  Error: {ex}")
        return False, None

def main():
    print("="*60)
    print("Kiss ASIS - Specialized Wiener Solver")
    print("="*60)
    
    attempts = 0
    while attempts < 100:
        attempts += 1
        print(f"\nAttempt {attempts}...")
        
        success, response = try_server()
        if success:
            print("\n" + "="*60)
            print("SUCCESS!")
            print(response)
            print("="*60)
            break
        
        time.sleep(0.5)
    
    print(f"\nTotal attempts: {attempts}")

if __name__ == "__main__":
    main()
