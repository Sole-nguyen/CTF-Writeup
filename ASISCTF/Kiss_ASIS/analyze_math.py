#!/usr/bin/env python3
"""
Analyze the exact relationship between e, d, and phi.
"""

from Crypto.Util.number import getPrime, inverse
from random import randint, uniform

def simulate():
    """Simulate challenge parameters locally"""
    nbit = 512  # Smaller for faster testing
    D = uniform(0.990, 0.999)
    k = randint(1, 6)
    
    dbit = int(nbit * D) + 1
    
    for _ in range(100):
        p = getPrime(nbit // 2)
        q = getPrime(nbit // 2)
        
        if p % 4 != 3 or q % 4 != 3:
            continue
            
        N = p * q
        if N.bit_length() != nbit:
            continue
            
        phi = (p ** k - 1) * (q ** k - 1)
        d = getPrime(dbit)
        
        if d.bit_length() != dbit:
            continue
        
        r = randint(0, 1)
        sigma = (-1) ** r  # 1 or -1
        
        x = phi + sigma * d
        
        try:
            e = inverse(x, phi)
        except:
            continue
        
        # Verify
        assert (e * x) % phi == 1
        assert (e * d * sigma) % phi == 1  # e * sigma * d ≡ 1 (mod phi)
        
        ed = e * d
        ed_mod_phi = ed % phi
        
        t = (ed - ed_mod_phi) // phi  # ed = t * phi + (ed mod phi)
        
        print(f"k={k}, sigma={sigma}")
        print(f"  N bits: {N.bit_length()}")
        print(f"  d bits: {d.bit_length()}")
        print(f"  phi bits: {phi.bit_length()}")
        print(f"  e bits: {e.bit_length()}")
        print(f"  t bits: {t.bit_length() if t > 0 else 0}")
        print(f"  e * d mod phi = {ed_mod_phi}")  # Should be 1 or phi-1
        print(f"  Expected: {1 if sigma == 1 else phi - 1}")
        print(f"  Match: {ed_mod_phi == 1 or ed_mod_phi == phi - 1}")
        print()
        
        # Check e approximation
        print(f"  phi / e = {phi // e}")
        print(f"  d = {d}")
        print(f"  Ratio phi/(e*d) = {phi / (e * d):.6f}")
        print()
        
        return

simulate()
