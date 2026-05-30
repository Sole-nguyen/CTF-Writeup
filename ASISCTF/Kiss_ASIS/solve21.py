#!/usr/bin/env python3
"""
Kiss ASIS - Multi-attack solver

Strategy:
1. Connect to server, get parameters
2. Determine k from e/N ratio
3. Try various attacks based on k value
4. Repeat until success

For k=1 specifically, we try:
- Wiener variants
- Continued fractions with phi approximations
- GCD-based attacks

For all k:
- Factor N directly (Fermat, Pollard rho, p-1)
- Check for weak primes
"""

from pwn import remote, context
import gmpy2
from gmpy2 import gcd, iroot, isqrt, mpz, is_prime, next_prime
from Crypto.Util.number import long_to_bytes
import time
import random
import traceback

context.log_level = 'error'

SERVER = "65.109.214.93"
PORT = 13137

def get_data():
    """Get N, e, enc from server"""
    r = remote(SERVER, PORT)
    
    r.recvuntil(b'[Q]uit')
    r.sendline(b'p')
    
    r.recvuntil(b'N = ')
    N = int(r.recvline().decode().strip())
    
    r.recvuntil(b'e = ')
    e = int(r.recvline().decode().strip())
    
    r.recvuntil(b'[Q]uit')
    r.sendline(b'e')
    r.recvuntil(b'enc = ')
    enc = int(r.recvline().decode().strip())
    
    return r, N, e, enc

def estimate_k(N, e):
    """Estimate k from bit lengths"""
    return max(1, min(6, round(e.bit_length() / N.bit_length())))

def fermat_factor(n, max_iter=100000):
    """Fermat factorization for close primes"""
    a = isqrt(n)
    if a * a == n:
        return a, a
    
    a += 1
    for i in range(max_iter):
        b2 = a * a - n
        b, is_sq = iroot(b2, 2)
        if is_sq:
            p = a + b
            q = a - b
            if p * q == n:
                return p, q
        a += 1
    return None, None

def pollard_rho(n, max_iter=500000):
    """Pollard rho factorization"""
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
        if 1 < d < n:
            return d, n // d
        if d == n:
            return None, None
    return None, None

def pollard_pm1(n, B=100000):
    """Pollard p-1 factorization for smooth p-1"""
    a = mpz(2)
    for p in range(2, B + 1):
        if is_prime(p):
            pp = p
            while pp <= B:
                a = pow(a, p, n)
                pp *= p
    
    d = gcd(a - 1, n)
    if 1 < d < n:
        return d, n // d
    return None, None

def try_cf_k1(N, e, enc):
    """Try continued fraction attack for k=1"""
    N = mpz(N)
    e = mpz(e)
    
    # Try multiple phi approximations
    sqrt_N = isqrt(N)
    
    for delta in range(-100, 101):
        phi_approx = N - 2 * sqrt_N + 1 + delta
        
        # Generate convergents
        p0, p1 = mpz(0), mpz(1)
        q0, q1 = mpz(1), mpz(0)
        
        n, d = mpz(e), mpz(phi_approx)
        
        for _ in range(10000):
            if d == 0:
                break
            a = n // d
            n, d = d, n - a * d
            
            p0, p1 = p1, a * p1 + p0
            q0, q1 = q1, a * q1 + q0
            
            t, d_cand = p1, q1
            
            if d_cand <= 1:
                continue
            
            if d_cand.bit_length() > N.bit_length() + 50:
                break
            
            # Check for valid factorization
            for eps in [1, -1]:
                val = e * d_cand - eps
                if val <= 0 or t == 0:
                    continue
                if val % t != 0:
                    continue
                
                phi_cand = val // t
                S = N - phi_cand + 1
                
                if S <= 0:
                    continue
                
                disc = S * S - 4 * N
                if disc < 0:
                    continue
                
                sq, is_sq = iroot(disc, 2)
                if not is_sq:
                    continue
                
                p = (S + sq) // 2
                q = (S - sq) // 2
                
                if p * q == N:
                    return int(p), int(q)
    
    return None, None

def try_factor(N, timeout=10):
    """Try various factorization methods"""
    start = time.time()
    
    # Fermat
    p, q = fermat_factor(N, 50000)
    if p:
        return p, q
    
    if time.time() - start > timeout:
        return None, None
    
    # Pollard rho
    p, q = pollard_rho(N, 100000)
    if p:
        return p, q
    
    if time.time() - start > timeout:
        return None, None
    
    # Pollard p-1
    p, q = pollard_pm1(N, 50000)
    if p:
        return p, q
    
    return None, None

def decrypt_k1(N, e, enc, p, q):
    """Decrypt for k=1 case"""
    phi = (p - 1) * (q - 1)
    d = int(gmpy2.invert(e, phi))
    m = pow(enc, d, N)
    return long_to_bytes(m)

def decrypt_generic(N, e, enc, p, q, k):
    """Decrypt for any k value"""
    # Standard RSA decryption uses phi(N) = (p-1)(q-1)
    # regardless of what k was used for key generation
    phi_N = (p - 1) * (q - 1)
    
    try:
        d = int(gmpy2.invert(e, phi_N))
        m = pow(enc, d, N)
        return long_to_bytes(m)
    except:
        return None

def submit(r, msg):
    """Submit answer to server"""
    try:
        r.recvuntil(b'[Q]uit', timeout=2)
        r.sendline(b's')
        r.recvuntil(b'message:', timeout=2)
        r.sendline(msg)
        
        response = r.recvall(timeout=5).decode()
        return response
    except:
        return ""

def main():
    print("Kiss ASIS Multi-Attack Solver v21")
    print("=" * 60)
    
    max_attempts = 200
    success_count = 0
    k_stats = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n[Attempt {attempt}/{max_attempts}]")
        
        try:
            r, N, e, enc = get_data()
            
            k_est = estimate_k(N, e)
            k_stats[k_est] = k_stats.get(k_est, 0) + 1
            
            print(f"  N: {N.bit_length()} bits, e: {e.bit_length()} bits, k~{k_est}")
            
            p, q = None, None
            
            # Strategy 1: Direct factorization (works for any k if N is weak)
            print(f"  [*] Trying direct factorization...", end=" ", flush=True)
            p, q = try_factor(N, timeout=3)
            if p:
                print("SUCCESS!")
            else:
                print("failed")
            
            # Strategy 2: CF attack for k=1
            if not p and k_est == 1:
                print(f"  [*] Trying CF attack for k=1...", end=" ", flush=True)
                p, q = try_cf_k1(N, e, enc)
                if p:
                    print("SUCCESS!")
                else:
                    print("failed")
            
            # If we found factors
            if p and q:
                print(f"  [+] Factored N!")
                print(f"      p: {int(p).bit_length()} bits")
                print(f"      q: {int(q).bit_length()} bits")
                
                # Try decryption
                msg = decrypt_generic(N, e, enc, int(p), int(q), k_est)
                
                if msg:
                    print(f"  [+] Decrypted: {msg}")
                    
                    # Check if printable
                    try:
                        if all(32 <= b < 127 for b in msg):
                            # Submit
                            response = submit(r, msg)
                            print(f"  [*] Server response: {response[:200]}")
                            
                            if 'flag' in response.lower() or 'asis' in response.lower():
                                print("\n" + "=" * 60)
                                print("FLAG FOUND!")
                                print(response)
                                print("=" * 60)
                                return
                    except:
                        pass
            
            r.close()
            
        except Exception as ex:
            print(f"  Error: {ex}")
            traceback.print_exc()
            continue
    
    print(f"\n[*] Completed {max_attempts} attempts")
    print(f"[*] k distribution: {k_stats}")

if __name__ == "__main__":
    main()
