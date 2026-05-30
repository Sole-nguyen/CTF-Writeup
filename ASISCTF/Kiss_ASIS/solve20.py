#!/usr/bin/env python3
"""
Kiss ASIS - Pure Python solver using continued fractions with sympy

Key insight: For k=1:
- phi = (p-1)(q-1) = N - S + 1, where S = p + q
- e*d = t*phi + eps, eps in {-1, 1}
- e/phi_approx should give t/d as convergent

We approximate phi with phi_approx = N - 2*sqrt(N) + 1
Then continued fractions of e/phi_approx should give us t/d.
"""

import json
import gmpy2
from gmpy2 import isqrt, mpz, is_prime
from fractions import Fraction
from Crypto.Util.number import long_to_bytes

def cf_convergents(num, den, max_iter=100000):
    """Generate convergents of num/den"""
    p0, p1 = mpz(0), mpz(1)
    q0, q1 = mpz(1), mpz(0)
    
    n, d = mpz(num), mpz(den)
    
    for _ in range(max_iter):
        if d == 0:
            break
        a = n // d
        n, d = d, n - a * d
        
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
        
        yield p1, q1

def try_convergent_k1(N, e, enc, t, d):
    """
    For a convergent t/d of e/phi_approx, check if it leads to valid p, q.
    """
    if d <= 1:
        return None
    
    N_bits = N.bit_length()
    d_bits = d.bit_length()
    
    # Check d is approximately correct size (~ N bits)
    if d_bits < N_bits - 100 or d_bits > N_bits + 50:
        return None
    
    # d should be prime - but checking is slow, so skip for now
    # We'll verify factorization instead
    
    # For e*d = t*phi + eps (eps = +/-1)
    # phi = (e*d - eps) / t
    
    for eps in [1, -1]:
        val = e * d - eps
        if val <= 0:
            continue
        if val % t != 0:
            continue
        
        phi_cand = val // t
        
        # For k=1: phi = N - S + 1, so S = N - phi + 1
        S = N - phi_cand + 1
        
        if S <= 0:
            continue
        
        # Check if S^2 - 4N is perfect square
        disc = S * S - 4 * N
        if disc < 0:
            continue
        
        sq, is_sq = gmpy2.iroot(disc, 2)
        if not is_sq:
            continue
        
        # Found valid p, q!
        p = (S + sq) // 2
        q = (S - sq) // 2
        
        if p * q != N:
            continue
        
        print(f"[+] Found factorization!")
        print(f"    p bits = {p.bit_length()}")
        print(f"    q bits = {q.bit_length()}")
        print(f"    d bits = {d.bit_length()}")
        
        # Decrypt with proper d
        phi_real = (int(p) - 1) * (int(q) - 1)
        d_real = gmpy2.invert(e, phi_real)
        m = pow(int(enc), int(d_real), int(N))
        
        try:
            msg = long_to_bytes(m)
            if all(32 <= b < 127 for b in msg):  # printable check
                print(f"    Decrypted: {msg}")
                return msg
            else:
                # Try without printable check
                print(f"    Raw bytes: {msg}")
                return msg
        except:
            print(f"    m = {m}")
    
    return None

def solve_k1(N, e, enc):
    """Try to solve for k=1 case using continued fractions"""
    N = mpz(N)
    e = mpz(e)
    enc = mpz(enc)
    
    N_bits = N.bit_length()
    e_bits = e.bit_length()
    
    k_est = round(e_bits / N_bits)
    
    print(f"N bits: {N_bits}")
    print(f"e bits: {e_bits}")
    print(f"Estimated k: {k_est}")
    
    if k_est != 1:
        print("Not k=1 case, skipping")
        return None
    
    # phi_approx = N - 2*sqrt(N) + 1
    sqrt_N = isqrt(N)
    phi_approx = N - 2 * sqrt_N + 1
    
    print(f"phi_approx bits: {phi_approx.bit_length()}")
    print()
    
    # Get convergents
    print("Checking continued fraction convergents...")
    
    count = 0
    for t, d in cf_convergents(e, phi_approx):
        count += 1
        if count % 1000 == 0:
            print(f"  Checked {count} convergents, current d bits: {d.bit_length()}")
        
        if d.bit_length() > N_bits + 100:
            print(f"  d too large ({d.bit_length()} bits), stopping")
            break
        
        result = try_convergent_k1(N, e, enc, t, d)
        if result:
            return result
    
    print(f"No solution found after {count} convergents")
    return None

def main():
    # Load samples
    samples_file = r'C:\Users\duynh\Documents\Code\CTF\ASISCTF\Kiss_ASIS\interesting_samples.json'
    
    try:
        with open(samples_file) as f:
            samples = json.load(f)
    except Exception as ex:
        print(f"Could not load {samples_file}: {ex}")
        return
    
    # Filter k=1 cases
    k1_samples = [s for s in samples if s.get('k_estimate', 0) == 1]
    print(f"Found {len(k1_samples)} k=1 samples\n")
    
    for i, s in enumerate(k1_samples[:5]):  # Try first 5
        print(f"{'='*60}")
        print(f"Trying sample {i+1}")
        print(f"{'='*60}")
        
        N = int(s['N'])
        e = int(s['e'])
        enc = int(s['enc'])
        
        result = solve_k1(N, e, enc)
        if result:
            print(f"\n[+] SUCCESS!")
            print(f"Message: {result}")
            break
        print()

if __name__ == "__main__":
    main()
