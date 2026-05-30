#!/usr/bin/env python3
"""
Kiss ASIS - Boneh-Durfee style attack

Key insight: e*d = 1 (mod phi_k) means e*d = k*phi_k + 1
For small k and known phi structure, we can use lattice methods.

For k_exp=2: phi = (p^2-1)(q^2-1) = (N+1)^2 - (p+q)^2
Let s = p + q, then phi = (N+1)^2 - s^2

e*d = t*((N+1)^2 - s^2) + eps
e*d - t*(N+1)^2 + t*s^2 = eps

This is a polynomial equation in t, d, s.
But s ~ 2*sqrt(N), d ~ N, t ~ N

Actually, there's a simpler approach for this specific problem.
"""

from Crypto.Util.number import *
from math import isqrt, gcd

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Trying direct brute force on S for k=2 with relaxed conditions")
print("="*60)

# For k=2: phi = (N+1)^2 - S^2
# e*d = t*phi + eps (eps = +/- 1)
# e*d = t*((N+1)^2 - S^2) + eps

# Given e and (N+1)^2 are known, for each candidate S:
# phi = (N+1)^2 - S^2
# We need e*d - eps to be divisible by phi
# i.e., (e*d - eps) mod phi = 0
# i.e., e*d mod phi = eps

# But we don't know d! However, if gcd(e, phi) = 1, then d = inverse(eps, phi) * eps
# Wait, that's wrong. Let me think again.

# e*d = t*phi + eps
# d = (t*phi + eps) / e

# For d to be an integer, (t*phi + eps) must be divisible by e
# So t*phi = -eps (mod e)
# t = -eps * inverse(phi, e) (mod e)

# So for each S (which gives phi), we can compute t mod e
# Then d = (t*phi + eps) / e

# The question is: how big is t?
# t = (e*d - eps) / phi
# e ~ 0.776 * N^2, d ~ N, phi ~ N^2
# t ~ 0.776 * N^2 * N / N^2 = 0.776 * N

# So t has about 1022 bits. t mod e gives us t since e > t (e has 2045 bits, t has 1022 bits)
# Wait no, e has 2045 bits so e > t. But phi also has about 2046 bits.
# t*phi ~ 1022 + 2046 = 3068 bits
# e*d ~ 2045 + 1023 = 3068 bits
# This matches!

# So for each S:
# 1. Compute phi = (N+1)^2 - S^2
# 2. If gcd(e, phi) != 1, skip
# 3. For eps in [1, -1]:
#    t = -eps * inverse(phi, e) mod e
#    d = (t*phi + eps) / e (should be exact)
#    Check if d is valid

N_plus_1_sq = (N+1)**2
sqrt_N = isqrt(N)

print(f"sqrt(N) = {sqrt_N.bit_length()} bits")
print(f"Searching S around 2*sqrt(N)...")

# S = p + q, where p, q are primes ~ 512 bits each
# S is around 2 * 2^511 = 2^512, but can vary

# disc = S^2 - 4N must be a perfect square for integer p, q
# So S^2 >= 4N, meaning S >= 2*sqrt(N)

S_min = 2 * sqrt_N
S_max = S_min + 10000000  # Search range

print(f"S range: {S_min} to {S_max}")
print(f"Searching {S_max - S_min} values...")

count = 0
for S in range(S_min, S_max):
    count += 1
    if count % 500000 == 0:
        print(f"Progress: {count}/{S_max - S_min}")
    
    phi = N_plus_1_sq - S * S
    if phi <= 0:
        continue
    
    g = gcd(e, phi)
    if g != 1:
        continue  # Can't compute inverse
    
    phi_inv_e = pow(phi, -1, e)  # inverse(phi, e)
    
    for eps in [1, -1]:
        t = (-eps * phi_inv_e) % e
        
        val = t * phi + eps
        if val <= 0:
            continue
        
        if val % e != 0:
            continue  # Should not happen if math is correct
        
        d = val // e
        
        # Check d size (should be ~1023-1024 bits)
        if d.bit_length() < 1000 or d.bit_length() > 1030:
            continue
        
        # Verify: e*d should equal t*phi + eps
        if e * d != t * phi + eps:
            continue
        
        # Check if S gives valid factorization
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
        print(f"    t = {t}")
        print(f"    eps = {eps}")
        
        # Verify phi
        phi_check = (p**2 - 1) * (q**2 - 1)
        print(f"    phi check: {phi == phi_check}")
        
        # Decrypt
        m = pow(enc, d, N)
        msg = long_to_bytes(m)
        print(f"    Decrypted: {msg}")
        exit()

print("\nNot found in search range.")
print("This suggests k != 2 or the search range is wrong.")
