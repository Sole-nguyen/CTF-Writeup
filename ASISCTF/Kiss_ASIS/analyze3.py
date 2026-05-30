#!/usr/bin/env python3
"""
Kiss ASIS - Analyze the math more carefully
"""

from Crypto.Util.number import *
from math import isqrt, gcd, log2

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Kiss ASIS Analysis")
print("="*60)

print(f"\nN bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")
print(f"enc bits: {enc.bit_length()}")

# Let's verify the relationship more carefully
# From the source: d is prime with ~1023 bits (nbit * D where D in [0.999, 0.9999])
# e = inverse(phi + (-1)^r * d, phi)
# This means: e * (phi + (-1)^r * d) = 1 (mod phi)
# => e * phi + e * (-1)^r * d = 1 (mod phi)
# => e * (-1)^r * d = 1 (mod phi)
# So: e * d = (-1)^r (mod phi)
# i.e., e * d = 1 (mod phi) or e * d = -1 (mod phi)

# This is standard RSA relationship!
# e * d = t * phi + 1  OR  e * d = t * phi - 1

# For k=1: phi = (p-1)(q-1), phi ~ N
# For k=2: phi = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1), phi ~ N^2
# For k=3: phi = (p^3-1)(q^3-1), phi ~ N^3
# etc.

# Given e ~ 2^2045 and d ~ 2^1023:
# e * d ~ 2^(2045+1023) = 2^3068

# For k=3: phi ~ N^3 ~ 2^(1023*3) = 2^3069
# So e * d / phi ~ 1, meaning t ~ 1

# But our search for t=1 didn't find anything...

# Let's check if maybe the problem is in our assumption about k
# e/N^k should give us a hint

print("\nAnalyzing e/N^k ratios:")
for k in range(1, 7):
    ratio = e / (N ** k)
    print(f"  k={k}: e/N^{k} = {ratio:.6f} (e/N^{k} bits: {log2(ratio) if ratio > 0 else 0:.1f})")

# The closest to 1 should indicate the right k
# For k=2: e/N^2 should be approximately t*phi_2/(d*N^2) = t*(N^2 - stuff)/(d*N^2) ~ t/d
# Since d ~ N, t/d ~ t/N which is tiny...

print("\nAnalyzing e*N^(-k) more carefully:")
for k in range(1, 7):
    # e / N^k should approximate some small multiple of 1/d
    ratio = e / (N ** k)
    # If e*d = t*phi_k + eps, and phi_k ~ N^k
    # then e ~ t*N^k/d
    # e/N^k ~ t/d
    # Since d ~ N, this would be ~ t/N
    
    # Let's compute what t would be if this k is correct
    # Assuming d ~ N: t ~ e * N / N^k = e / N^(k-1)
    t_estimate = e / (N ** (k-1))
    print(f"  k={k}: t estimate (if d~N) = {t_estimate:.3f}")

# Hmm, for k=2: t ~ e/N ~ N^2/N = N = huge
# For k=3: t ~ e/N^2 ~ 1 (since e ~ N^2)
# This confirms k=3 with t ~ 1

print("\n" + "="*60)
print("So k=3, t~1 is the right direction")
print("Let's verify the math for k=3 again")
print("="*60)

# For k=3:
# phi = (p^3-1)(q^3-1) 
#     = p^3*q^3 - p^3 - q^3 + 1
#     = N^3 - (p^3 + q^3) + 1

# p^3 + q^3 = (p+q)(p^2 - pq + q^2)
#           = S * ((p+q)^2 - 3pq)
#           = S * (S^2 - 3N)
# where S = p + q

# So phi = N^3 - S(S^2 - 3N) + 1 = N^3 - S^3 + 3NS + 1

# e*d = t*phi + r where r = +1 or -1 (for the original r in source)
# Wait, let's check this again from source:
# e = inverse(phi + (-1)^r * d, phi)
# So e * (phi + (-1)^r * d) = 1 (mod phi)
# e * phi + e * (-1)^r * d = 1 (mod phi)
# e * (-1)^r * d = 1 (mod phi)
# So e * d = (-1)^r (mod phi)
# If r is random 0 or 1:
#   r=0: e*d = 1 (mod phi)
#   r=1: e*d = -1 (mod phi) = phi - 1 (mod phi)

# So e*d = k*phi + 1 or e*d = k*phi - 1 for some integer k
# (k here is the quotient, not the exponent!)

# Given that e ~ N^2 and d ~ N and phi ~ N^3,
# e*d ~ N^3 ~ phi, so k ~ 1

# Let me search more carefully around t=1

print("\nSearching with t=1, varying delta more carefully...")

N3 = N ** 3

for t in [1]:
    for r in [1, -1]:
        print(f"\nTrying t={t}, r={r}:")
        # e * d = t * phi + r
        # d = (t * phi + r) / e
        
        # phi = N^3 - S^3 + 3NS + 1
        # S ranges around 2*sqrt(N)
        
        sqrt_N = isqrt(N)
        S_min = int(1.9 * sqrt_N)
        S_max = int(2.1 * sqrt_N)
        
        print(f"  Searching S from {S_min} to {S_max} (range: {S_max - S_min})")
        
        count = 0
        for S in range(S_min, S_max + 1):
            count += 1
            if count % 1000000 == 0:
                print(f"    Progress: {count} / {S_max - S_min}")
            
            phi = N3 - S**3 + 3*N*S + 1
            
            d_times_e = t * phi + r
            if d_times_e <= 0:
                continue
            
            if d_times_e % e != 0:
                continue
            
            d = d_times_e // e
            
            # Check if d is reasonable (should be ~1023 bits and prime)
            if d.bit_length() < 1000 or d.bit_length() > 1030:
                continue
            
            # Check if S gives valid p, q
            disc = S*S - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (S + sqrt_disc) // 2
            q = (S - sqrt_disc) // 2
            
            if p * q != N:
                continue
            
            print(f"\n[+] FOUND!")
            print(f"    S = {S}")
            print(f"    p = {p}")
            print(f"    q = {q}")
            print(f"    d = {d}")
            
            # Verify
            phi_check = (p**3 - 1) * (q**3 - 1)
            print(f"    phi_check == phi: {phi_check == phi}")
            print(f"    e*d mod phi = {(e*d) % phi}")
            
            # Decrypt
            d_real = inverse(e, phi)
            m = pow(enc, d_real, N)
            print(f"    Decrypted: {long_to_bytes(m)}")
            exit()
        
        print(f"  Searched {count} values of S")

print("\nNo solution found with t=1")

# The issue is that (t*phi + r) must be divisible by e
# e is huge (2045 bits), so this is rare
# We need to search for the right S that makes this work

# Alternative: use the fact that e*d - r is divisible by phi
# e*d = r (mod phi)
# For a given d, we can check if (e*d - r) / phi is an integer

print("\n" + "="*60)
print("Alternative: Search for d directly")
print("="*60)

# d is a random prime of about 1023 bits
# We can't enumerate all such primes, but...

# Actually, let's think about this differently
# From e = inverse(phi + sign*d, phi), we have:
# gcd(phi + sign*d, phi) = gcd(sign*d, phi) = gcd(d, phi)
# For inverse to exist, gcd(d, phi) = 1
# Since d is prime and phi = (p^k-1)(q^k-1), we need d to not divide phi

# The key insight: e*d = 1 (mod phi) or e*d = -1 (mod phi)
# Means e*d = q*phi + eps for some q, eps in {1, -1}

# Since e ~ N^2 and d ~ N and phi ~ N^3:
# e*d ~ N^3 ~ phi
# So q should be ~ 1 or 2

# Let me try q = 1, 2, 3... with a smarter search

print("\nTrying with phi calculated from assumed p,q relations...")

# Actually, we've been searching S but the issue is e | (t*phi + r)
# This is a very restrictive condition

# Let's try: factor e or check if e has special structure
print(f"\nChecking if e has small factors:")
for small_p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    if e % small_p == 0:
        print(f"  e is divisible by {small_p}")

g = gcd(e, N)
print(f"gcd(e, N) = {g}")

g = gcd(e, N - 1)
print(f"gcd(e, N-1) = {g}")

g = gcd(e, N + 1)
print(f"gcd(e, N+1) = {g}")
