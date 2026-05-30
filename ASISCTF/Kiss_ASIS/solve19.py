#!/usr/bin/env python3
"""
Kiss ASIS - Specifically target k=1 cases using Boneh-Durfee like approach
For k=1: phi = (p-1)(q-1) = N - S + 1 where S = p + q
e * d = t * phi +- 1

Since e is the inverse of (phi +- d) mod phi, we have:
e * (phi +- d) = 1 + m * phi  for some m
=> e * d = 1 - m*phi + e*phi = 1 + (e - m)*phi  (if sign is +)
or e * d = 1 + m*phi - e*phi = 1 + (m - e)*phi  (if sign is -)

So t = e - m or t = m - e.

Key observation: if d ~ N and phi ~ N, then e * d ~ e * N
And e * d = t * phi + eps ~ t * N

So t ~ e (same order of magnitude).

For k=1, e should be around phi/2 or less.

Let me try to find k=1 cases and apply Wiener's extended attack.
"""

from pwn import remote, context
import gmpy2
from gmpy2 import gcd, iroot, isqrt
from math import log2
from sympy import nextprime, isprime, factorint
from Crypto.Util.number import long_to_bytes

context.log_level = 'error'

SERVER = "65.109.214.93"
PORT = 13137

def get_data():
    """Get N, e, enc from server"""
    r = remote(SERVER, PORT)
    
    # Get public params
    r.recvuntil(b'[Q]uit')
    r.sendline(b'p')
    
    line = r.recvuntil(b'N = ').decode()
    N_line = r.recvline().decode().strip()
    N = int(N_line)
    
    e_line = r.recvuntil(b'e = ').decode()
    e_data = r.recvline().decode().strip()
    e = int(e_data)
    
    # Get encrypted message
    r.recvuntil(b'[Q]uit')
    r.sendline(b'e')
    r.recvuntil(b'enc = ')
    enc = int(r.recvline().decode().strip())
    
    return r, N, e, enc

def estimate_k(N, e):
    """Estimate k from e size"""
    N_bits = N.bit_length()
    e_bits = e.bit_length()
    
    # For k: phi ~ N^k, so e ~ N^k
    # e_bits / N_bits ~ k
    ratio = e_bits / N_bits
    k_est = round(ratio)
    return max(1, min(6, k_est))

def cf_convergents(n, d, max_iter=100000):
    """Generate convergents of n/d"""
    p0, p1 = 0, 1
    q0, q1 = 1, 0
    
    for _ in range(max_iter):
        if d == 0:
            break
        a = n // d
        n, d = d, n - a * d
        
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        
        yield p1, q1

def wiener_attack_k1(N, e, max_convergents=10000):
    """
    Wiener attack for k=1.
    
    For standard RSA: e*d = 1 + k*phi where phi = N - S + 1
    Continued fraction of e/N gives approximation k/d.
    
    But in this challenge: e*d = t*phi +- 1
    So we try e/N and e/(N+1) etc.
    """
    
    for base in [N, N-1, N+1, N//2]:
        for p_k, q_d in cf_convergents(e, base, max_convergents):
            if q_d == 0 or p_k == 0:
                continue
            
            # q_d is our candidate for d
            d_cand = q_d
            
            if d_cand.bit_length() < 1000 or d_cand.bit_length() > 1040:
                continue
            
            # Check if d is prime (rough test)
            if d_cand < 2:
                continue
            
            # Try both epsilon = +1 and -1
            for eps in [1, -1]:
                # e*d = t*phi + eps
                # => phi = (e*d - eps) / t = (e*d - eps) / p_k
                if p_k == 0:
                    continue
                    
                val = e * d_cand - eps
                if val <= 0 or val % p_k != 0:
                    continue
                
                phi_cand = val // p_k
                
                # For k=1: phi = N - S + 1, so S = N - phi + 1
                S = N - phi_cand + 1
                
                if S <= 0 or S * S < 4 * N:
                    continue
                
                # Check if S^2 - 4N is perfect square
                disc = S * S - 4 * N
                if disc < 0:
                    continue
                    
                sq, is_sq = iroot(disc, 2)
                if is_sq:
                    p = (S + int(sq)) // 2
                    q = (S - int(sq)) // 2
                    
                    if p * q == N:
                        print(f"[+] Found factors with Wiener!")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        print(f"    d = {d_cand}")
                        return p, q, d_cand
    
    return None, None, None

def extended_gcd_attack(N, e):
    """
    Try to find d using extended GCD relationships.
    
    We know: e * (phi +- d) = 1 mod phi
    Which means: e * d = +- 1 mod phi
    
    Let's try: gcd(e - 1, N^2 - 1) or similar.
    """
    
    for k in range(1, 7):
        # For each k, try to find patterns in e
        Nk = pow(N, k)
        
        # Check GCD patterns
        for offset in [1, -1, 0]:
            g = gcd(e + offset, Nk - 1)
            if g > 1 and g.bit_length() > 100:
                print(f"  k={k}: gcd(e{'+' if offset>=0 else ''}{offset}, N^{k}-1) = {g.bit_length()} bits")

def try_all_attacks(N, e, enc):
    """Try all available attacks"""
    
    k_est = estimate_k(N, e)
    print(f"  Estimated k = {k_est}")
    print(f"  N bits = {N.bit_length()}, e bits = {e.bit_length()}")
    
    # Only proceed with k=1 cases
    if k_est != 1:
        print(f"  [!] k != 1, skipping Wiener (not applicable)")
        return None
    
    print(f"  [*] Trying Wiener attack for k=1...")
    p, q, d = wiener_attack_k1(N, e)
    
    if p and q:
        # Decrypt
        phi = (p - 1) * (q - 1)
        d_real = gmpy2.invert(e, phi)
        m = pow(enc, int(d_real), N)
        msg = long_to_bytes(int(m))
        return msg
    
    print(f"  [!] Wiener attack failed")
    
    # Try extended GCD patterns
    print(f"  [*] Checking GCD patterns...")
    extended_gcd_attack(N, e)
    
    return None

def main():
    print("Kiss ASIS Solver v19 - Target k=1 cases")
    print("=" * 60)
    
    max_attempts = 100  # Try many connections to find k=1
    k1_count = 0
    
    for attempt in range(max_attempts):
        print(f"\nAttempt {attempt + 1}/{max_attempts}...")
        
        try:
            r, N, e, enc = get_data()
            
            k_est = estimate_k(N, e)
            
            if k_est == 1:
                k1_count += 1
                print(f"  [!] Found k=1 case! (total k=1: {k1_count})")
                
                result = try_all_attacks(N, e, enc)
                
                if result:
                    print(f"\n[+] Decrypted message: {result}")
                    
                    # Submit
                    r.recvuntil(b'[Q]uit')
                    r.sendline(b's')
                    r.recvuntil(b'message:')
                    r.sendline(result)
                    
                    response = r.recvall(timeout=5).decode()
                    print(f"Server response: {response}")
                    
                    if 'flag' in response.lower():
                        print(f"\n{'='*60}")
                        print(f"FLAG FOUND!")
                        print(response)
                        return
            else:
                print(f"  k~{k_est}, skipping")
            
            r.close()
            
        except Exception as ex:
            print(f"  Error: {ex}")
            continue
    
    print(f"\n[*] Completed {max_attempts} attempts. Found {k1_count} k=1 cases.")

if __name__ == "__main__":
    main()
