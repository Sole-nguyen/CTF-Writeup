#!/usr/bin/env python3
"""
Kiss ASIS - Better approach using continued fractions
"""

from Crypto.Util.number import *
from math import gcd, isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

# For k=2: phi = (p^2-1)(q^2-1)
# e*d = t*phi ± 1
# If d ≈ N (about 1023 bits) and phi ≈ N^2 (about 2046 bits)
# Then e*d ≈ N^3 (about 3068 bits)
# So t*phi ≈ N^3, meaning t ≈ N (about 1023 bits)
# 
# Wait, that's not small t. Let me reconsider.

# Actually, let's look at the bit sizes:
# e = 2045 bits
# d = 1023 bits (since D ≈ 0.999 and nbit = 1024)
# e*d = 2045 + 1023 = 3068 bits
#
# For k=2: phi = (p^2-1)(q^2-1) 
# p, q ≈ 512 bits each
# p^2, q^2 ≈ 1024 bits each
# phi ≈ (p^2)(q^2) = N^2 ≈ 2046 bits
#
# e*d = t*phi ± 1
# 3068 bits ≈ t * 2046 bits
# t ≈ 2^(3068-2046) = 2^1022 bits
#
# So for k=2, t is huge (not small)

# Let me reconsider the problem...
# Looking at the code again:
# e = inverse(phi + (-1)**r * d, phi)
# This gives: e * (phi + (-1)^r * d) ≡ 1 (mod phi)
# => e * (-1)^r * d ≡ 1 (mod phi)
# => e * d ≡ (-1)^r (mod phi)
#
# So e*d = t*phi + (-1)^r for some integer t >= 1
#
# Key insight: e is computed as inverse of (phi ± d) mod phi
# Since d can be up to about phi (when D ≈ 1), the value phi ± d could be:
# - If d < phi: phi + d or phi - d are both positive and less than 2*phi
# - The inverse exists if gcd(phi ± d, phi) = 1, which is true if gcd(d, phi) = 1

# Since d is prime and large, gcd(d, phi) = 1 is almost certain

# Now, e = inverse(phi ± d, phi)
# e * (phi ± d) ≡ 1 (mod phi)
# e * (phi ± d) = k * phi + 1 for some k
#
# Since phi ± d < 2*phi (when d < phi), we have:
# e * (phi ± d) = k * phi + 1
# where k depends on the size of e
#
# If e is large (close to phi), then e * (phi ± d) ≈ phi * (phi ± d) ≈ phi^2
# So k ≈ phi * (1 ± d/phi) ≈ phi

# OK this is getting complex. Let me try a different approach.

# The key observation from the code:
# e = inverse(phi + (-1)**r * d, phi)
#
# Let's call X = phi + (-1)^r * d
# Then e*X ≡ 1 (mod phi)
# So e*X = m*phi + 1 for some integer m >= 1
#
# Substituting X:
# e*(phi + (-1)^r * d) = m*phi + 1
# e*phi + e*(-1)^r*d = m*phi + 1
# e*(-1)^r*d = (m-e)*phi + 1
#
# Let T = m - e
# e*(-1)^r*d = T*phi + 1
#
# If r = 0: e*d = T*phi + 1
# If r = 1: -e*d = T*phi + 1, so e*d = -T*phi - 1

# So we have:
# e*d = ±T*phi ± 1

# For the attack to work, |T| should be small.

# When is T small?
# T = m - e
# e*X = m*phi + 1
# m = (e*X - 1) / phi
# T = (e*X - 1)/phi - e = (e*X - 1 - e*phi) / phi = (e*(X - phi) - 1) / phi = (e*(-1)^r*d - 1) / phi
#
# So T = (e*(-1)^r*d - 1) / phi
# Or e*d = T*phi + (-1)^(r+1)

# For T to be small (≈ 1), we need:
# e*d ≈ phi
# With d ≈ N and e having 2045 bits:
# e*d ≈ e*N
# For this to equal phi = (p^k-1)(q^k-1) ≈ N^k:
# e*N ≈ N^k
# e ≈ N^(k-1)
#
# e has 2045 bits, N has 1023 bits
# N^(k-1) has 1023*(k-1) bits
# For e ≈ N^(k-1): 2045 ≈ 1023*(k-1)
# k-1 ≈ 2, so k ≈ 3

# But wait, k is chosen from 1 to 6. And e has 2045 bits = 2*1023 bits ≈ N^2 bits
# So k-1 = 2, meaning k = 3

# For k=3:
# phi = (p^3-1)(q^3-1) ≈ N^3 (3069 bits)
# e*d ≈ N^3 with e ≈ N^2 and d ≈ N
# Hmm, N^2 * N = N^3, which matches phi!

# So for k=3:
# e*d ≈ phi (with T ≈ 1)
# e*d = T*phi ± 1 where T = 1 or T = 2

# Let's verify with the actual numbers:
N3 = N ** 3
print(f"\nN^3 bits: {N3.bit_length()}")

# Estimate: e*d ≈ phi ≈ N^3
# d ≈ N^3 / e

d_estimate = N3 // e
print(f"d_estimate = N^3 / e = {d_estimate}")
print(f"d_estimate bits: {d_estimate.bit_length()}")

# For k=3, let's define the solve function
def solve_cubic_s(N, phi):
    """
    For k=3, phi = (p^3 - 1)(q^3 - 1) = N^3 - (p^3 + q^3) + 1
    p^3 + q^3 = (p+q)^3 - 3pq(p+q) = S^3 - 3NS where S = p+q
    So: phi = N^3 - S^3 + 3NS + 1
    Rearranging: S^3 - 3NS = N^3 + 1 - phi
    
    This returns S = p + q if found
    """
    RHS = N**3 + 1 - phi
    
    # S^3 - 3*N*S = RHS
    # We need to solve for S
    
    # Initial guess: S ≈ 2*sqrt(N)
    S = 2 * isqrt(N)
    
    # Newton-Raphson
    for _ in range(200):
        f = S**3 - 3*N*S - RHS
        fp = 3*S**2 - 3*N
        if fp == 0:
            break
        S_new = S - f // fp
        if abs(S_new - S) <= 1:
            # Try S_new, S_new-1, S_new+1
            for delta in range(-2, 3):
                SS = S_new + delta
                if SS > 0 and SS**3 - 3*N*SS == RHS:
                    return SS
            break
        S = S_new
    
    return None

def factor_from_S(N, S):
    """Given S = p + q and N = p*q, find p and q"""
    disc = S*S - 4*N
    if disc < 0:
        return None, None
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None, None
    p = (S + sqrt_disc) // 2
    q = (S - sqrt_disc) // 2
    if p * q == N:
        return max(p, q), min(p, q)
    return None, None

# Try different k values and T values
print("\n" + "="*60)
print("Searching for factors...")
print("="*60)

found = False
for k in [3, 2, 4, 1, 5, 6]:
    if found:
        break
    print(f"\nTrying k = {k}")
    
    Nk = N ** k
    d_est = Nk // e
    
    print(f"  d estimate (N^{k}/e): {d_est.bit_length()} bits")
    
    # Search around d_est with different T values
    for T in range(1, 50):
        if found:
            break
        for sign in [1, -1]:
            if found:
                break
                
            # e*d = T*phi + sign
            # phi = (e*d - sign) / T
            
            # But we don't know d exactly. Let's try:
            # From phi ≈ N^k and e*d = T*phi + sign
            # d ≈ (T*N^k + sign) / e
            
            d_candidate = (T * Nk + sign) // e
            
            # Check if this d gives a valid factorization
            if d_candidate <= 0:
                continue
                
            phi_candidate = (e * d_candidate - sign)
            if phi_candidate % T != 0:
                # Try adjusting d
                for delta in range(-5, 6):
                    d_try = d_candidate + delta
                    if d_try <= 0:
                        continue
                    for s2 in [sign, -sign]:
                        phi_try = e * d_try - s2
                        if phi_try > 0 and phi_try % T == 0:
                            phi_actual = phi_try // T
                            
                            if k == 3:
                                S = solve_cubic_s(N, phi_actual)
                                if S:
                                    p, q = factor_from_S(N, S)
                                    if p and q:
                                        print(f"\n[+] FOUND! k={k}, T={T}, sign={s2}, delta={delta}")
                                        print(f"    d = {d_try}")
                                        print(f"    p = {p}")
                                        print(f"    q = {q}")
                                        found = True
                                        break
                            elif k == 2:
                                # phi = (p^2-1)(q^2-1) = N^2 - (p^2+q^2) + 1
                                # p^2 + q^2 = (p+q)^2 - 2N = S^2 - 2N
                                # phi = N^2 - S^2 + 2N + 1 = (N+1)^2 - S^2
                                # S^2 = (N+1)^2 - phi
                                S_sq = (N+1)**2 - phi_actual
                                if S_sq > 0:
                                    S = isqrt(S_sq)
                                    if S * S == S_sq:
                                        p, q = factor_from_S(N, S)
                                        if p and q:
                                            print(f"\n[+] FOUND! k={k}, T={T}, sign={s2}, delta={delta}")
                                            print(f"    d = {d_try}")
                                            print(f"    p = {p}")
                                            print(f"    q = {q}")
                                            found = True
                                            break
                    if found:
                        break
                continue
            
            phi_actual = phi_candidate // T
            
            if k == 3:
                S = solve_cubic_s(N, phi_actual)
                if S:
                    p, q = factor_from_S(N, S)
                    if p and q:
                        print(f"\n[+] FOUND! k={k}, T={T}, sign={sign}")
                        print(f"    d = {d_candidate}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        found = True
            elif k == 2:
                S_sq = (N+1)**2 - phi_actual
                if S_sq > 0:
                    S = isqrt(S_sq)
                    if S * S == S_sq:
                        p, q = factor_from_S(N, S)
                        if p and q:
                            print(f"\n[+] FOUND! k={k}, T={T}, sign={sign}")
                            print(f"    d = {d_candidate}")
                            print(f"    p = {p}")
                            print(f"    q = {q}")
                            found = True
