#!/usr/bin/env python3
"""
Kiss ASIS - Wiener-like attack for large e
Based on: e*d = 1 (mod phi) implies e*d = k*phi + 1
For k=3: phi = (p^3-1)(q^3-1) approx N^3 - N^2 - N
"""

from Crypto.Util.number import *
from math import isqrt, gcd

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

# First let's understand the relationship better
# e*d = 1 + k*phi  OR  e*d = -1 + k*phi (for r=1 vs r=-1)
# For k_exp = 3:
#   phi_k = (p^3-1)(q^3-1) = p^3*q^3 - p^3 - q^3 + 1
#                         = N^3 - (p^3 + q^3) + 1
# where p^3 + q^3 = (p+q)^3 - 3pq(p+q) = (p+q)^3 - 3N(p+q)

# Let s = p + q
# phi_k = N^3 - s^3 + 3Ns + 1

# From d having about 1023 bits and N being 1023 bits, d is approx N
# e = 2045 bits, N^2 = 2046 bits, so e is approx N^2

# This means: e*d approx k * phi_k
# For k_exp=3: phi_k approx N^3
# So e*d approx k * N^3
# N^2 * N = N^3
# So k should be around 1!

print("\nChecking if e*d approx N^3...")
print(f"e bits: {e.bit_length()}")
print(f"N^2 bits: {(N*N).bit_length()}")
print(f"N^3 bits: {(N**3).bit_length()}")

# If k=1: e*d approx phi_3 approx N^3
# d approx N^3/e = N^3/N^2 = N (1023 bits) - matches!

# Now the continued fractions approach:
# e/N^3 is approximately k/d * (phi/N^3) 
# Since phi/N^3 approx 1, e/N^3 approx k/d

def continued_fraction(num, denom, limit=200):
    """Get continued fraction coefficients"""
    cf = []
    while denom != 0 and len(cf) < limit:
        q = num // denom
        cf.append(q)
        num, denom = denom, num - q * denom
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

print("\n" + "="*60)
print("Trying Wiener attack on e/N^3...")
print("="*60)

for k_exp in [3, 2, 4, 5, 6, 1]:
    print(f"\nTrying k_exp = {k_exp}...")
    Nk = N ** k_exp
    
    # e / N^k should be close to k/d where e*d = k*phi + eps
    cf = continued_fraction(e, Nk, 500)
    
    count = 0
    for k_guess, d_guess in convergents(cf):
        if d_guess == 0 or k_guess == 0:
            continue
        
        count += 1
        if count > 10000:
            break
        
        d = d_guess
        
        # Check if d works
        for r in [1, -1]:
            val = e * d - r
            if val <= 0:
                continue
            
            # val = k * phi
            # Try small k values
            for k_mult in range(1, 50):
                if val % k_mult != 0:
                    continue
                phi = val // k_mult
                
                if phi <= 0:
                    continue
                
                # For k_exp = 1: phi = (p-1)(q-1) = N - (p+q) + 1
                # p + q = N + 1 - phi
                if k_exp == 1:
                    S = N + 1 - phi
                    if S <= 0:
                        continue
                    disc = S*S - 4*N
                    if disc < 0:
                        continue
                    sqrt_disc = isqrt(disc)
                    if sqrt_disc * sqrt_disc != disc:
                        continue
                    p = (S + sqrt_disc) // 2
                    q = (S - sqrt_disc) // 2
                    if p > 0 and q > 0 and p * q == N:
                        print(f"[+] FOUND with k_exp={k_exp}, k_mult={k_mult}, r={r}")
                        print(f"    d = {d}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        break
                
                # For k_exp = 2: phi = (p^2-1)(q^2-1) = N^2 - (p^2 + q^2) + 1
                # p^2 + q^2 = (p+q)^2 - 2pq = S^2 - 2N
                # phi = N^2 - S^2 + 2N + 1
                # S^2 = N^2 + 2N + 1 - phi = (N+1)^2 - phi
                elif k_exp == 2:
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
                    if p > 0 and q > 0 and p * q == N:
                        print(f"[+] FOUND with k_exp={k_exp}, k_mult={k_mult}, r={r}")
                        print(f"    d = {d}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        break

# Also try directly with e/phi_approx where phi_approx = N^k - stuff
print("\n" + "="*60)
print("Trying alternative approach - estimate phi more precisely")
print("="*60)

for k_exp in [3]:
    print(f"\nFor k_exp = {k_exp}:")
    # phi = (p^k - 1)(q^k - 1) = N^k - (p^k + q^k) + 1
    # p^k + q^k is hard to estimate but we know p, q are roughly sqrt(N)
    # If p approx q approx sqrt(N), then p^k + q^k approx 2 * N^(k/2)
    
    Nk = N ** k_exp
    
    # For k=3, p^3 + q^3 = (p+q)^3 - 3pq(p+q) = s^3 - 3Ns
    # s = p + q is roughly 2*sqrt(N)
    s_approx = 2 * isqrt(N)
    pk_qk_approx = s_approx**k_exp - 3*N*s_approx  # only valid for k=3
    
    phi_approx = Nk - pk_qk_approx + 1
    print(f"  phi_approx bits: {phi_approx.bit_length()}")
    
    # e / phi_approx should be close to k/d
    cf = continued_fraction(e, phi_approx, 500)
    
    print("  Checking convergents...")
    count = 0
    for k_guess, d_guess in convergents(cf):
        if d_guess == 0:
            continue
        count += 1
        if count > 5000:
            break
        
        d = d_guess
        
        # d should be prime and about 1023 bits
        if d.bit_length() < 1000 or d.bit_length() > 1030:
            continue
        
        for r in [1, -1]:
            val = e * d - r
            if val <= 0:
                continue
            
            for k_mult in range(1, 20):
                if val % k_mult != 0:
                    continue
                phi = val // k_mult
                
                # phi = N^3 - s^3 + 3Ns + 1
                # s^3 - 3Ns = N^3 + 1 - phi
                RHS = N**3 + 1 - phi
                
                # Solve s^3 - 3Ns - RHS = 0 using Newton
                s = s_approx
                for _ in range(100):
                    f = s**3 - 3*N*s - RHS
                    fp = 3*s*s - 3*N
                    if fp == 0:
                        break
                    s_new = s - f // fp
                    if abs(s_new - s) <= 1:
                        break
                    s = s_new
                
                # Check nearby values
                for ds in range(-10, 11):
                    S = s + ds
                    if S <= 0:
                        continue
                    if S**3 - 3*N*S != RHS:
                        continue
                    
                    disc = S*S - 4*N
                    if disc < 0:
                        continue
                    sqrt_disc = isqrt(disc)
                    if sqrt_disc * sqrt_disc != disc:
                        continue
                    
                    p = (S + sqrt_disc) // 2
                    q = (S - sqrt_disc) // 2
                    
                    if p > 0 and q > 0 and p * q == N:
                        print(f"[+] FOUND with k_exp={k_exp}, k_mult={k_mult}, r={r}")
                        print(f"    d = {d}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        
                        # Decrypt
                        phi_real = (p**k_exp - 1) * (q**k_exp - 1)
                        d_real = inverse(e, phi_real)
                        m = pow(enc, d_real, N)
                        print(f"    msg: {long_to_bytes(m)}")
                        exit()

print("\nDone searching.")
