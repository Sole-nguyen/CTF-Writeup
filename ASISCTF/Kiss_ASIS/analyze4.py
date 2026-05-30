#!/usr/bin/env python3
"""
Kiss ASIS - k=2 analysis
e/N^2 = 0.775871, meaning e ~ 0.78 * N^2
If phi_2 ~ N^2 and e*d = t*phi + eps, with d ~ N:
  e*d ~ 0.78 * N^2 * N = 0.78 * N^3
  t*phi ~ 0.78 * N^3
  If phi ~ N^2, then t ~ 0.78 * N
  
That's a huge t! But wait - let's reconsider.
"""

from Crypto.Util.number import *
from math import isqrt, gcd
from fractions import Fraction

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Kiss ASIS - Reconsidering the attack")
print("="*60)

N2 = N * N
N3 = N ** 3

# e/N^2 = 0.775871
ratio = Fraction(e, N2)
print(f"\nExact ratio e/N^2 = {float(ratio):.10f}")
print(f"e = {ratio.numerator}")
print(f"N^2 = {ratio.denominator}")

# Key insight: e * d = t * phi + eps
# For k=2: phi_2 = (p^2-1)(q^2-1) 
#         = p^2*q^2 - p^2 - q^2 + 1
#         = N^2 - (p^2 + q^2) + 1
#         = N^2 - (p+q)^2 + 2pq + 1
#         = N^2 - S^2 + 2N + 1
#         = N^2 + 2N + 1 - S^2
#         = (N+1)^2 - S^2

# So phi_2 = (N+1)^2 - S^2 = (N+1-S)(N+1+S)

# Now, S = p + q where p, q are 512-bit primes
# S is roughly 2 * 2^511 = 2^512

print(f"\n(N+1)^2 = {(N+1)**2}")
print(f"N^2 bits: {N2.bit_length()}")
print(f"(N+1)^2 bits: {((N+1)**2).bit_length()}")

# For k=2, if p,q are balanced (both ~512 bits):
# S ~ 2 * sqrt(N) ~ 2^513
# S^2 ~ 2^1026
# But (N+1)^2 ~ N^2 ~ 2^2046
# So phi_2 ~ N^2 - 2^1026 ~ N^2 (1 - 1/N) ~ N^2

# So actually phi_2 is VERY close to N^2!
# phi_2 / N^2 ~ 1 - S^2/N^2 ~ 1 - 4N/N^2 = 1 - 4/N ~ 1

sqrt_N = isqrt(N)
S_approx = 2 * sqrt_N
S_approx_sq = S_approx ** 2

print(f"\nsqrt(N) ~ 2^{sqrt_N.bit_length()}")
print(f"S_approx = 2*sqrt(N) ~ 2^{S_approx.bit_length()}")
print(f"S_approx^2 bits: {S_approx_sq.bit_length()}")
print(f"N^2 bits: {N2.bit_length()}")

phi2_approx = (N+1)**2 - S_approx_sq
print(f"\nphi_2_approx (using S~2*sqrt(N)): {phi2_approx.bit_length()} bits")
print(f"phi_2_approx / N^2 = {float(Fraction(phi2_approx, N2)):.10f}")

# So phi_2 is about 1 - eps times N^2 where eps is tiny
# Given e/N^2 = 0.776, we have e = 0.776 * N^2

# e*d = t*phi_2 + eps
# 0.776 * N^2 * d = t * phi_2 + eps
# 0.776 * N^2 * d = t * N^2 * (1 - delta) + eps  (where delta is tiny)
# 0.776 * d = t * (1 - delta) + eps/N^2
# 0.776 * d ~ t

# If d ~ N:
# t ~ 0.776 * N ~ a huge number!

print("\n" + "="*60)
print("Hmm, but wait - let's reconsider d's size")
print("="*60)

# From source: d = getRandomRange(2^(nbit * D), 2^((nbit+1) * D))
# where D is in [0.999, 0.9999] and nbit = 1024
# So d is between 2^(1024*0.999) and 2^(1025*0.9999)
# i.e., between 2^1022.976 and 2^1024.8975
# So d is around 1023-1025 bits

# Also d must be prime (getPrime)
# So d is a random ~1023-1024 bit prime

# Given e has 2045 bits and N has 1023 bits:
# If k=2: phi_2 ~ N^2 has ~2046 bits
# e*d ~ 2045 + 1023 = 3068 bits
# t*phi_2 ~ t * 2046 bits
# For e*d = t*phi_2 + eps, we need t ~ 2^1022

# This means t is also about 1023 bits! A huge search space...

print("\nIf k=2:")
print(f"  e bits: {e.bit_length()}")
print(f"  d bits: ~1023-1024")
print(f"  e*d bits: ~3068")
print(f"  phi_2 bits: ~{phi2_approx.bit_length()}")
print(f"  t must be: ~{3068 - phi2_approx.bit_length()} bits = ~1022 bits")

# That's too big to search directly

# But there's a key relationship we can exploit!
# e/phi_2 ~ t/d
# And we want t and d to be coprime (probably)

# Actually, let's think about continued fractions on e/phi_2_approx
# If e/phi_2 ~ t/d, then convergents should give us candidates

print("\n" + "="*60)  
print("Trying continued fractions on e / phi_2_approx")
print("="*60)

def continued_fraction(num, denom, limit=500):
    cf = []
    while denom != 0 and len(cf) < limit:
        q = num // denom
        cf.append(q)
        num, denom = denom, num - q * denom
    return cf

def convergents(cf):
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    for a in cf:
        h2 = a * h1 + h0
        k2 = a * k1 + k0
        yield (h2, k2)
        h0, h1 = h1, h2
        k0, k1 = k1, k2

# Use several phi approximations
for S_mult in [1.99, 1.999, 2.0, 2.001, 2.01]:
    S_test = int(S_mult * sqrt_N)
    phi_test = (N+1)**2 - S_test**2
    
    if phi_test <= 0:
        continue
    
    print(f"\nUsing S = {S_mult}*sqrt(N), phi_approx has {phi_test.bit_length()} bits")
    
    cf = continued_fraction(e, phi_test, 500)
    
    found = False
    for t_cand, d_cand in convergents(cf):
        if d_cand == 0:
            continue
        
        # Check if d_cand is reasonable size
        if d_cand.bit_length() < 1010 or d_cand.bit_length() > 1030:
            continue
        
        # t should also be ~1022 bits
        if t_cand.bit_length() < 1010:
            continue
        
        # Check: e*d = t*phi + eps for some reasonable phi
        # We need to find the real phi from the equation
        
        for eps in [1, -1]:
            val = e * d_cand - eps
            if val <= 0:
                continue
            if val % t_cand != 0:
                continue
            
            phi = val // t_cand
            
            # For k=2: phi = (N+1)^2 - S^2
            # S^2 = (N+1)^2 - phi
            S_sq = (N+1)**2 - phi
            if S_sq <= 0:
                continue
            S = isqrt(S_sq)
            if S * S != S_sq:
                continue
            
            # Check p, q
            disc = S*S - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (S + sqrt_disc) // 2
            q = (S - sqrt_disc) // 2
            
            if p * q == N:
                print(f"[+] FOUND! t={t_cand.bit_length()} bits, d={d_cand.bit_length()} bits")
                print(f"    p = {p}")
                print(f"    q = {q}")
                found = True
                
                # Decrypt
                phi_real = (p**2 - 1) * (q**2 - 1)
                d_real = inverse(e, phi_real)
                m = pow(enc, d_real, N)
                print(f"    msg: {long_to_bytes(m)}")
                break
        
        if found:
            break
    
    if found:
        break

if not found:
    print("\nContinued fractions didn't work directly.")
    
# Let's try a different approach: since e/N^2 ~ 0.776
# and we expect e*d = t*phi + eps
# Let's compute e*d for various d and see if it's close to a multiple of phi

print("\n" + "="*60)
print("Checking GCD patterns")  
print("="*60)

# For k=2: phi = (N+1)^2 - S^2 = (N+1-S)(N+1+S)
# (N+1-S) = (N+1) - (p+q) = N + 1 - p - q = (N-p) + (1-q) = q(p/q - 1) + 1 - q
# Hmm this is getting complicated

# Let's try: gcd(e, (N+1)^2 - 1) etc.
print(f"gcd(e, N^2-1) = {gcd(e, N**2 - 1)}")
print(f"gcd(e, (N+1)^2) = {gcd(e, (N+1)**2)}")
print(f"gcd(e, (N-1)^2) = {gcd(e, (N-1)**2)}")

# Maybe e and N share structure
print(f"\ngcd(e, N) = {gcd(e, N)}")
print(f"gcd(e-1, N) = {gcd(e-1, N)}")
print(f"gcd(e+1, N) = {gcd(e+1, N)}")

# Check if e-1 or e+1 has N as factor
print(f"\n(e-1) % N = {(e-1) % N}")
print(f"(e+1) % N = {(e+1) % N}")

# Check divisibility
print(f"\ne % (N-1) = {e % (N-1)}")
print(f"e % (N+1) = {e % (N+1)}")
