#!/usr/bin/env sage
"""
Kiss ASIS - Complete SageMath solver with LLL

For k=1:
- phi = (p-1)(q-1) = N - S + 1, where S = p + q
- e*d = t*phi + eps, eps in {-1, 1}

Rearranging:
e*d - t*(N-S+1) = eps
e*d - t*N + t*S - t = eps

Let's build a lattice. We seek small solutions (d, t, S) to:
e*d - t*N + t*S - t - eps = 0

This has a bilinear term t*S which makes it hard.

Alternative approach for k=1:
Since e ~ N/2 and d ~ N, we have e*d ~ N^2/2.
And phi ~ N, so t ~ e*d/phi ~ N.

The relationship e*d = t*phi + eps gives:
e*d/phi = t + eps/phi ~ t (since eps/phi ~ 0)

So t ~ e*d/phi ~ e (since d ~ phi for k=1).

For Boneh-Durfee attack, we need d to be small (d < N^0.292).
But here d ~ N, so standard Boneh-Durfee doesn't apply.

For this specific challenge, the insight is:
- e = inverse(phi + sigma*d, phi) where sigma = +/-1
- This means e*(phi + sigma*d) = 1 (mod phi)
- So e*sigma*d = 1 (mod phi), i.e., e*d = sigma (mod phi)

The key insight is that d is PRIME!
So we need: d is prime, d ~ N, and e*d = t*phi + sigma.

Strategy: Use the continued fraction of e/phi_approx where phi_approx = N - 2*sqrt(N) + 1

For k=1:
- phi = (p-1)(q-1) = N - (p+q) + 1
- p+q ~ 2*sqrt(N) (with some error)
- phi ~ N - 2*sqrt(N) + 1

Let phi_approx = N - 2*isqrt(N) + 1
Then e/phi_approx should be close to t/d.

Let's try this approach!
"""

from sage.all import *
import json
import sys

# Load sample data
samples_file = "interesting_samples.json"

def isqrt(n):
    """Integer square root"""
    if n < 0:
        raise ValueError("Square root of negative number")
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def cf_convergents(num, den):
    """Generate convergents of num/den"""
    cf = continued_fraction(Rational(num)/Rational(den))
    return cf.convergents()

def try_convergent_k1(N, e, enc, conv):
    """
    For a convergent t/d of e/phi_approx, check if it leads to valid p, q.
    """
    t = conv.numerator()
    d = conv.denominator()
    
    if d <= 1:
        return None
        
    # Check d is approximately correct size (~ N bits)
    if d.nbits() < N.nbits() - 50 or d.nbits() > N.nbits() + 10:
        return None
    
    # d should be prime
    if not is_prime(d):
        return None
    
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
        disc = S*S - 4*N
        if disc < 0:
            continue
            
        sq = isqrt(disc)
        if sq * sq != disc:
            continue
        
        # Found valid p, q!
        p = (S + sq) // 2
        q = (S - sq) // 2
        
        if p * q != N:
            continue
            
        print(f"[+] Found factorization!")
        print(f"    p = {p}")
        print(f"    q = {q}")
        print(f"    d = {d}")
        
        # Decrypt
        m = pow(enc, int(d), int(N))
        try:
            msg = bytes.fromhex(hex(m)[2:])
            print(f"    Decrypted: {msg}")
            return msg
        except:
            print(f"    m = {m}")
            # Try different d
            # d_real = inverse_mod(e, phi_cand)
            # m = pow(enc, int(d_real), int(N))
    
    return None

def solve_k1(N, e, enc):
    """Try to solve for k=1 case using continued fractions"""
    N = Integer(N)
    e = Integer(e)
    enc = Integer(enc)
    
    # phi_approx = N - 2*sqrt(N) + 1
    sqrt_N = isqrt(N)
    phi_approx = N - 2 * sqrt_N + 1
    
    print(f"N bits: {N.nbits()}")
    print(f"e bits: {e.nbits()}")
    print(f"Estimated k: {round(e.nbits() / N.nbits())}")
    
    if round(e.nbits() / N.nbits()) != 1:
        print("Not k=1 case, skipping")
        return None
    
    print("phi_approx bits:", phi_approx.nbits())
    print()
    
    # Get convergents
    print("Computing continued fraction convergents...")
    convs = list(cf_convergents(e, phi_approx))
    print(f"Got {len(convs)} convergents")
    
    for i, conv in enumerate(convs):
        if i % 100 == 0:
            print(f"Checking convergent {i}/{len(convs)}...")
        
        result = try_convergent_k1(N, e, enc, conv)
        if result:
            return result
    
    print("No solution found with continued fractions")
    return None

def main():
    # Load samples
    try:
        with open(samples_file) as f:
            samples = json.load(f)
    except:
        print(f"Could not load {samples_file}")
        return
    
    # Filter k=1 cases
    k1_samples = [s for s in samples if s.get('k_estimate', 0) == 1]
    print(f"Found {len(k1_samples)} k=1 samples")
    
    for i, s in enumerate(k1_samples[:5]):  # Try first 5
        print(f"\n{'='*60}")
        print(f"Trying sample {i+1}")
        print(f"{'='*60}")
        
        N = Integer(s['N'])
        e = Integer(s['e'])
        enc = Integer(s['enc'])
        
        result = solve_k1(N, e, enc)
        if result:
            print(f"\n[+] SUCCESS!")
            print(f"Message: {result}")
            break

if __name__ == "__main__":
    main()
