#!/usr/bin/env python3
"""
Kiss ASIS - Debug analysis
Let's understand the relationship between e, d, N, and phi
"""

from Crypto.Util.number import *
from math import gcd, isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")
print(f"e/N bit ratio: {e.bit_length() / N.bit_length():.3f}")

# D = uniform(0.9990, 0.9999)
# dbit = int(nbit * D) + 1 where nbit = 1024
# So dbit is in range [int(1024 * 0.999) + 1, int(1024 * 0.9999) + 1] = [1023, 1024]
print(f"\nd is a prime with about 1023-1024 bits")

# e = inverse(phi + (-1)^r * d, phi)
# This means: e * (phi + (-1)^r * d) ≡ 1 (mod phi)
# => e * phi + e * (-1)^r * d ≡ 1 (mod phi)
# => e * (-1)^r * d ≡ 1 (mod phi)
# => e * d ≡ (-1)^r (mod phi) where r ∈ {0, 1}
#
# So: e * d = t * phi + (-1)^r for some integer t
#
# Now, phi = (p^k - 1) * (q^k - 1)
# For k=1: phi ≈ N
# For k=2: phi ≈ N^2
# For k=3: phi ≈ N^3
# etc.

# Given e has 2045 bits and d has ~1023 bits:
# e * d has about 2045 + 1023 = 3068 bits
print(f"\ne * d would have about {e.bit_length()} + 1023 = {e.bit_length() + 1023} bits")

# For k=1: phi ≈ N has 1023 bits
# e * d = t * phi + r
# 3068 bits = t * 1023 bits => t has about 2045 bits - very large
print(f"\nFor k=1: t would have about {3068 - 1023} = 2045 bits (too large)")

# For k=2: phi ≈ N^2 has 2046 bits
# e * d = t * phi + r
# 3068 bits = t * 2046 bits => t has about 1022 bits - still large
print(f"For k=2: t would have about {3068 - 2046} = 1022 bits (still large)")

# For k=3: phi ≈ N^3 has 3069 bits
# e * d = t * phi + r
# 3068 bits ≈ t * 3069 bits => t ≈ 1 (very small!)
print(f"For k=3: t would be about 1 (perfect!)")

# So k=3 is the likely candidate!
# With t ≈ 1, we have: e * d ≈ phi ± 1
# phi = (p^3 - 1) * (q^3 - 1)

print("\n" + "="*60)
print("Analysis suggests k=3 with t=1")
print("="*60)

# For k=3:
# phi = (p^3 - 1)(q^3 - 1) = p^3*q^3 - p^3 - q^3 + 1 = N^3 - (p^3 + q^3) + 1
#
# Let's use the identity: p^3 + q^3 = (p+q)^3 - 3pq(p+q) = (p+q)^3 - 3N(p+q)
# Let S = p + q
# p^3 + q^3 = S^3 - 3NS
# phi = N^3 - S^3 + 3NS + 1
#
# From e*d = phi + r (assuming t=1), we get:
# phi = e*d - r where r = ±1
#
# We need to find d such that:
# 1) d is prime with ~1023 bits
# 2) phi = e*d - r makes sense as (p^3-1)(q^3-1) for some p,q with p*q = N

# From phi = N^3 - S^3 + 3NS + 1 and phi = e*d - r:
# N^3 - S^3 + 3NS + 1 = e*d - r
# N^3 + 3NS + 1 + r = e*d + S^3
# 
# This is still tricky because we have two unknowns: d and S

# Alternative approach: Wiener's attack variant
# e*d ≡ ±1 (mod phi)
# Since d ≈ N and phi ≈ N^3, we have e ≈ N^2
# 
# Let's verify: e has 2045 bits, N^2 has 2046 bits - close!

N_squared = N * N
print(f"\nN^2 bits: {N_squared.bit_length()}")
print(f"e bits: {e.bit_length()}")

# The key insight: e/phi ≈ 1/d (approximately)
# e * d ≈ phi
# e/phi ≈ 1/d

# For k=3: phi ≈ N^3
# e/(N^3) ≈ 1/d

N_cubed = N * N * N
ratio = e / N_cubed
print(f"\ne / N^3 ≈ {ratio}")
print(f"1/ratio ≈ {1/ratio}")
print(f"Expected d ≈ 1/ratio = {int(1/ratio)}")

d_estimate = int(N_cubed / e)
print(f"\nAlternative d estimate = N^3 / e = {d_estimate}")
print(f"d_estimate bits: {d_estimate.bit_length()}")

# That looks more reasonable! d should be around 1023 bits

# Now let's search around this d estimate
print("\n" + "="*60)
print("Searching for correct d around estimate...")
print("="*60)

def try_solve_for_k3(N, e, d):
    """
    For k=3, check if d gives valid factorization.
    phi = (p^3 - 1)(q^3 - 1)
    e*d = phi ± 1 (assuming t=1)
    """
    for r in [1, -1]:
        phi = e * d - r
        
        if phi <= 0:
            continue
        
        # phi = N^3 - S^3 + 3NS + 1 where S = p + q
        # Rearranging: S^3 - 3NS = N^3 + 1 - phi
        # S^3 - 3NS - (N^3 + 1 - phi) = 0
        #
        # This is a cubic in S. Let's try to solve it.
        
        RHS = N**3 + 1 - phi
        # S^3 - 3*N*S - RHS = 0
        
        # For a cubic a*x^3 + b*x^2 + c*x + d = 0
        # We have: S^3 + 0*S^2 - 3N*S - RHS = 0
        # a=1, b=0, c=-3N, d=-RHS
        
        # Using the cubic formula is complex. Let's try Newton-Raphson.
        # f(S) = S^3 - 3*N*S - RHS
        # f'(S) = 3*S^2 - 3*N
        
        # Initial guess: S ≈ 2*sqrt(N) (since p,q ≈ sqrt(N))
        S = 2 * isqrt(N)
        
        for _ in range(100):
            f = S**3 - 3*N*S - RHS
            fp = 3*S**2 - 3*N
            if fp == 0:
                break
            S_new = S - f // fp
            if S_new == S:
                break
            S = S_new
        
        # Check if S is correct
        if S**3 - 3*N*S == RHS or (S+1)**3 - 3*N*(S+1) == RHS or (S-1)**3 - 3*N*(S-1) == RHS:
            # Adjust S if needed
            for delta in [-1, 0, 1]:
                SS = S + delta
                if SS**3 - 3*N*SS == RHS:
                    S = SS
                    break
            else:
                continue
            
            # Now we have S = p + q
            # p + q = S
            # p * q = N
            # Solving: x^2 - S*x + N = 0
            disc = S*S - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (S + sqrt_disc) // 2
            q = (S - sqrt_disc) // 2
            
            if p * q == N:
                return p, q, d, r
    
    return None

# Search around d_estimate
print(f"Searching around d = {d_estimate}...")

found = False
for delta in range(-500000, 500001):
    if delta % 50000 == 0:
        print(f"  Trying delta = {delta}...")
    
    d_try = d_estimate + delta
    if d_try <= 0:
        continue
    
    result = try_solve_for_k3(N, e, d_try)
    if result:
        p, q, d, r = result
        print(f"\n[+] FOUND!")
        print(f"    delta = {delta}")
        print(f"    d = {d}")
        print(f"    r = {r}")
        print(f"    p = {p}")
        print(f"    q = {q}")
        print(f"    p * q = N: {p * q == N}")
        found = True
        break

if not found:
    print("\nNot found in this range. Trying wider search or different approach...")
    
    # Maybe try continued fractions on e/N^3
    print("\nTrying continued fractions on e/N^3...")
    
    from math import gcd
    
    # Compute convergents of e/N^3
    a, b = e, N_cubed
    convergents = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    
    while b and len(convergents) < 300:
        q = a // b
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        convergents.append((h_curr, k_curr))
        a, b = b, a % b
    
    print(f"Generated {len(convergents)} convergents")
    
    for i, (h, k) in enumerate(convergents):
        # k might be related to d, and h might be related to 1
        # Since e/N^3 ≈ 1/d, we expect k ≈ d for some convergent
        
        d_candidate = k
        if d_candidate.bit_length() < 1020 or d_candidate.bit_length() > 1030:
            continue
        
        result = try_solve_for_k3(N, e, d_candidate)
        if result:
            p, q, d, r = result
            print(f"\n[+] FOUND via continued fraction!")
            print(f"    convergent {i}: h={h}, k={k}")
            print(f"    d = {d}")
            print(f"    r = {r}")
            print(f"    p = {p}")
            print(f"    q = {q}")
            break
