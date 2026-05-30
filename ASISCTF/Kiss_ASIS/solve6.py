#!/usr/bin/env python3
"""
Kiss ASIS - Correct Analysis

Key equations:
- d is a random prime with ~1023-1024 bits
- phi = (p^k - 1) * (q^k - 1)
- e = inverse(phi + (-1)^r * d, phi)

This means:
e * (phi + (-1)^r * d) ≡ 1 (mod phi)
e * (-1)^r * d ≡ 1 (mod phi)
e * d ≡ (-1)^r (mod phi)

So: e * d = t * phi + (-1)^r for some integer t ≥ 1

Given:
- N = 1024 bits
- d = 1023-1024 bits (random prime)
- e = ? (we need to analyze)

For each k:
- k=1: phi ≈ N (1023 bits)
- k=2: phi ≈ N^2 (2046 bits)  
- k=3: phi ≈ N^3 (3069 bits)
- etc.

Since e*d = t*phi ± 1:
- If t is small (like 1), then e*d ≈ phi
- With d ≈ N, we get e ≈ phi/N = N^(k-1)

From the example:
- e has 2045 bits ≈ N^2 bits
- This suggests k=3 (so e ≈ N^2 when d ≈ N and phi ≈ N^3)

OR it could be k=2 with t being larger!

Let me analyze more carefully:
For k=2: phi ≈ N^2 ≈ 2046 bits
With t small: e*d ≈ t*phi, so e ≈ t*N^2/N = t*N ≈ t*1023 bits

For e to have 2045 bits with t*1023: t ≈ 2, but that gives ~1023 bits, not 2045!

Actually: e has 2045 bits, d has 1023 bits
e*d ≈ 2^(2045+1023) = 2^3068 bits product

For k=2: phi ≈ 2^2046
e*d ≈ t*phi implies t ≈ 2^(3068-2046) = 2^1022 ≈ N

So t ≈ N, which is huge!

For k=3: phi ≈ 2^3069
e*d ≈ t*phi implies t ≈ 2^(3068-3069) = 2^(-1) < 1

This means t = 0 or t = 1. If t = 1:
e*d ≈ phi ≈ N^3

With d ≈ N: e ≈ N^2, which matches (2045 bits)!

So k=3 with t=1 is the right hypothesis!
"""

from Crypto.Util.number import *
from math import gcd, isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

# For k=3: 
# e*d = t*phi + r where t = 1 and r = ±1
# phi = (p^3 - 1)(q^3 - 1)

# We use continued fractions on e / N^3 to find d
# Since e*d ≈ phi ≈ N^3, we have e/N^3 ≈ 1/d
# So the convergents of e/N^3 approximate 1/d

print("\n" + "="*60)
print("Attack: Using continued fractions on e / N^3")
print("="*60)

N3 = N ** 3

def cf_attack(num, den):
    """Generate convergents and test them"""
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    a, b = num, den
    
    while b:
        q = a // b
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        
        # h_curr / k_curr is a convergent of num/den
        # For e/N^3 ≈ 1/d, we might have k_curr = d
        
        yield h_curr, k_curr
        
        a, b = b, a % b

def factor_from_phi_k3(N, phi):
    """
    For k=3: phi = (p^3-1)(q^3-1)
    phi = N^3 - (p^3 + q^3) + 1
    p^3 + q^3 = (p+q)^3 - 3pq(p+q) = S^3 - 3NS
    So: S^3 - 3NS = N^3 + 1 - phi
    """
    RHS = N**3 + 1 - phi
    
    # Solve S^3 - 3NS = RHS using Newton-Raphson
    S = 2 * isqrt(N)
    
    for iteration in range(500):
        f = S**3 - 3*N*S - RHS
        fp = 3*S**2 - 3*N
        if fp == 0:
            break
        
        delta = f // fp
        if delta == 0:
            break
        S = S - delta
    
    # Check S and nearby values
    for ds in range(-20, 21):
        SS = S + ds
        if SS <= 0:
            continue
        if SS**3 - 3*N*SS == RHS:
            # Found S = p + q!
            disc = SS*SS - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            p = (SS + sqrt_disc) // 2
            q = (SS - sqrt_disc) // 2
            if p * q == N and isPrime(p) and isPrime(q):
                return p, q
    return None, None

# Run attack
print("\nGenerating convergents of e / N^3...")

count = 0
for h, k in cf_attack(e, N3):
    count += 1
    if count > 2000:
        break
    
    # k might be d (denominator)
    d_candidate = k
    
    # Also try h as d
    for d_try in [k, h]:
        if d_try.bit_length() < 1018 or d_try.bit_length() > 1030:
            continue
        
        # e*d = t*phi + r, try t=1 and r=±1
        for t in [1, 2]:
            for r in [1, -1]:
                phi_times_t = e * d_try - r
                if phi_times_t <= 0 or phi_times_t % t != 0:
                    continue
                phi = phi_times_t // t
                
                p, q = factor_from_phi_k3(N, phi)
                if p and q:
                    print(f"\n[+] FOUND! (convergent {count})")
                    print(f"    t = {t}, r = {r}")
                    print(f"    d = {d_try}")
                    print(f"    phi = {phi}")
                    print(f"    p = {p}")
                    print(f"    q = {q}")
                    
                    # Verify
                    phi_check = (p**3 - 1) * (q**3 - 1)
                    print(f"    phi check: {phi == phi_check}")
                    
                    # Decrypt
                    d_real = inverse(e, phi_check)
                    m = pow(enc, d_real, N)
                    msg = long_to_bytes(m)
                    print(f"    Decrypted: {msg}")
                    exit(0)

print(f"\nTried {count} convergents, no luck.")

# Alternative: try k=2
print("\n" + "="*60)
print("Trying k=2...")
print("="*60)

N2 = N ** 2

for h, k in cf_attack(e, N2):
    count += 1
    if count > 4000:
        break
    
    for d_try in [k, h]:
        if d_try.bit_length() < 1018 or d_try.bit_length() > 1030:
            continue
        
        for t in range(1, 100):
            for r in [1, -1]:
                phi_times_t = e * d_try - r
                if phi_times_t <= 0 or phi_times_t % t != 0:
                    continue
                phi = phi_times_t // t
                
                # For k=2: phi = (N+1)^2 - S^2
                S_sq = (N+1)**2 - phi
                if S_sq <= 0:
                    continue
                S = isqrt(S_sq)
                if S * S != S_sq:
                    continue
                
                disc = S*S - 4*N
                if disc < 0:
                    continue
                sqrt_disc = isqrt(disc)
                if sqrt_disc * sqrt_disc != disc:
                    continue
                
                p = (S + sqrt_disc) // 2
                q = (S - sqrt_disc) // 2
                
                if p * q == N:
                    print(f"\n[+] FOUND with k=2!")
                    print(f"    t = {t}, r = {r}")
                    print(f"    d = {d_try}")
                    print(f"    p = {p}")
                    print(f"    q = {q}")
                    
                    phi_check = (p**2 - 1) * (q**2 - 1)
                    d_real = inverse(e, phi_check)
                    m = pow(enc, d_real, N)
                    msg = long_to_bytes(m)
                    print(f"    Decrypted: {msg}")
                    exit(0)

print("\nAttack failed for this instance.")
print("The parameters might not be vulnerable to this approach.")
print("Try connecting to the server for a new instance.")
