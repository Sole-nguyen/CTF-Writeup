#!/usr/bin/env python3
"""
Kiss ASIS - Collect multiple samples and find patterns
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import time
import json

context.log_level = 'error'

def get_params():
    """Get N, e, enc from server"""
    try:
        io = remote("65.109.214.93", 13137, timeout=20)
        io.recvuntil(b"[Q]uit", timeout=10)
        io.sendline(b"p")
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        
        N, e = None, None
        for line in data.split("\n"):
            if "N = " in line: N = int(line.split("N = ")[1].strip())
            if "e = " in line: e = int(line.split("e = ")[1].strip())
        
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        
        enc = None
        for line in data.split("\n"):
            if "enc = " in line: enc = int(line.split("enc = ")[1].strip())
        
        io.close()
        return N, e, enc
    except Exception as ex:
        return None, None, None

def analyze_sample(N, e, enc):
    """Analyze a sample"""
    n_bits = N.bit_length()
    e_bits = e.bit_length()
    
    # Estimate k
    k_estimate = round(e_bits / n_bits)
    if k_estimate == 0:
        k_estimate = 1
    
    # Check GCDs
    g_n1 = gcd(e, N+1)
    g_n1_sq = gcd(e, (N+1)**2)
    g_nm1 = gcd(e, N-1)
    g_n2m1 = gcd(e, N**2 - 1)
    
    # Check N mod 7
    n_mod_7 = N % 7
    
    return {
        "n_bits": n_bits,
        "e_bits": e_bits,
        "k_estimate": k_estimate,
        "gcd_N+1": g_n1,
        "gcd_(N+1)^2": g_n1_sq,
        "gcd_N-1": g_nm1,
        "gcd_N^2-1": g_n2m1,
        "N_mod_7": n_mod_7,
        "N": N,
        "e": e,
        "enc": enc
    }

def try_factor(N, timeout_iters=50000):
    """Quick factorization attempt"""
    # Fermat
    a = isqrt(N) + 1
    for i in range(min(10000, timeout_iters)):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            return a - b, a + b
        a += 1
    
    # Pollard rho
    x, y, d = 2, 2, 1
    f = lambda x: (x*x + 1) % N
    for i in range(timeout_iters):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x-y), N)
        if d != 1 and d != N:
            return d, N // d
    
    return None, None

def main():
    print("="*70)
    print("Kiss ASIS - Sample Collection and Analysis")
    print("="*70)
    
    samples = []
    
    for i in range(30):
        print(f"\nSample {i+1}...")
        
        N, e, enc = get_params()
        if N is None:
            print("  Failed to get params")
            time.sleep(1)
            continue
        
        analysis = analyze_sample(N, e, enc)
        samples.append(analysis)
        
        print(f"  N bits: {analysis['n_bits']}, e bits: {analysis['e_bits']}, k~{analysis['k_estimate']}")
        print(f"  gcd(e,N+1)={analysis['gcd_N+1']}, gcd(e,(N+1)^2)={analysis['gcd_(N+1)^2']}")
        print(f"  N mod 7 = {analysis['N_mod_7']}")
        
        # If k=1 (e ~ N), try harder factorization
        if analysis['k_estimate'] == 1:
            print("  K=1 detected! Trying factorization...")
            p, q = try_factor(N, 200000)
            if p:
                print(f"  FACTORED! p has {p.bit_length()} bits")
                analysis['p'] = p
                analysis['q'] = q
        
        # If unusual GCD pattern
        if analysis['gcd_N+1'] > 1 or analysis['gcd_N-1'] > 1:
            print(f"  Interesting GCD pattern! Trying factorization...")
            p, q = try_factor(N, 200000)
            if p:
                print(f"  FACTORED! p has {p.bit_length()} bits")
                analysis['p'] = p
                analysis['q'] = q
        
        time.sleep(0.3)
    
    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    
    k_counts = {}
    for s in samples:
        k = s['k_estimate']
        k_counts[k] = k_counts.get(k, 0) + 1
    
    print(f"K distribution: {k_counts}")
    
    # Check for any factored samples
    factored = [s for s in samples if 'p' in s]
    if factored:
        print(f"\nFactored {len(factored)} samples!")
        for s in factored:
            print(f"  Sample: p={s['p']}, q={s['q']}")
    else:
        print("\nNo samples factored :(")
    
    # Save samples with interesting properties
    interesting = [s for s in samples if s['k_estimate'] == 1 or s['gcd_N+1'] > 1]
    if interesting:
        print(f"\n{len(interesting)} interesting samples saved")
        # Save to file (convert to string for JSON)
        for s in interesting:
            s['N'] = str(s['N'])
            s['e'] = str(s['e'])
            s['enc'] = str(s['enc'])
        with open('interesting_samples.json', 'w') as f:
            json.dump(interesting, f, indent=2)

if __name__ == "__main__":
    main()
