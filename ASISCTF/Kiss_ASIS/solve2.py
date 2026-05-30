#!/usr/bin/env python3
"""
Kiss ASIS - Improved solver
Key insight: When d is very large (D ≈ 0.999), we have e*d ≈ phi
For k > 1, phi = (p^k - 1)(q^k - 1) is much larger than N
The relationship e*d = t*phi ± 1 with small t allows us to recover phi
"""

from Crypto.Util.number import *
from math import gcd, isqrt

def try_factor_phi(phi_candidate, N, k):
    """
    phi = (p^k - 1)(q^k - 1) = p^k * q^k - p^k - q^k + 1
    Let X = p^k, Y = q^k
    X * Y = N^k
    X + Y = N^k + 1 - phi
    So X and Y are roots of: t^2 - (N^k + 1 - phi)*t + N^k = 0
    """
    Nk = N ** k
    sum_XY = Nk + 1 - phi_candidate
    prod_XY = Nk
    
    # t^2 - sum_XY * t + prod_XY = 0
    disc = sum_XY * sum_XY - 4 * prod_XY
    if disc < 0:
        return None, None
    
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None, None
    
    X = (sum_XY + sqrt_disc) // 2
    Y = (sum_XY - sqrt_disc) // 2
    
    if X * Y != prod_XY:
        return None, None
    
    # Now X = p^k, Y = q^k
    # Find k-th roots
    for pk, qk in [(X, Y), (Y, X)]:
        p = round(pk ** (1/k))
        for delta in range(-10, 11):
            pp = p + delta
            if pp > 1 and pp ** k == pk:
                q = N // pp
                if pp * q == N:
                    return min(pp, q), max(pp, q)
    
    return None, None

def attack(N, e):
    """Main attack"""
    print(f"[*] N bits: {N.bit_length()}")
    print(f"[*] e bits: {e.bit_length()}")
    
    # e/N bit ratio tells us about k
    ratio = e.bit_length() / N.bit_length()
    print(f"[*] e/N bit ratio: {ratio:.3f}")
    
    # For k=2, phi ≈ N^2 and d ≈ N, so e ≈ N
    # For k=3, phi ≈ N^3 and d ≈ N, so e ≈ N^2
    # etc.
    
    for k in range(1, 7):
        print(f"\n[*] Trying k = {k}")
        
        # phi = (p^k - 1)(q^k - 1)
        # e * d ≡ ±1 (mod phi)
        # e * d = t * phi ± 1
        
        # Since d is a prime with about 1024 * 0.999 ≈ 1023 bits
        # and e*d ≈ t * phi where phi ≈ N^k
        
        # We try small t values
        for t in range(1, 30):
            for sign in [1, -1]:
                # We need to estimate d
                # d ≈ N^D where D ≈ 0.999
                # Let's try d around N
                
                # e * d = t * phi + sign
                # d = (t * phi + sign) / e
                
                # Since phi = (p^k-1)(q^k-1) and p,q ≈ sqrt(N)
                # phi ≈ N^k
                
                # So d ≈ t * N^k / e
                
                # For this to work, we iterate over possible d values
                # But d is about 1023-1024 bits, so instead:
                
                # Use: e*d - sign = t * phi
                # phi = (p^k - 1)(q^k - 1)
                # 
                # If we knew d, we could compute phi and factor it.
                # Since we don't know d exactly, we estimate:
                
                # d_min ≈ 2^1022, d_max ≈ 2^1024
                d_bits_min = int(1024 * 0.999)
                d_bits_max = 1024
                
                # For each d bit length, the corresponding phi is:
                # phi ≈ (e * 2^d_bits - sign) / t
                
                for d_bits in range(d_bits_min, d_bits_max + 1):
                    d_approx = (1 << d_bits) + (1 << (d_bits - 1))  # roughly 1.5 * 2^d_bits
                    
                    phi_approx = (e * d_approx - sign) // t
                    
                    # Check if this phi could factor as (p^k-1)(q^k-1)
                    p, q = try_factor_phi(phi_approx, N, k)
                    if p and q and p * q == N:
                        print(f"[+] Found with k={k}, t={t}, sign={sign}, d_bits={d_bits}")
                        return p, q
        
        # Try direct formula approach
        # Assume t = 1 (most common case)
        # e * d = phi ± 1
        # phi = (p^k - 1)(q^k - 1)
        #
        # Since d is prime with ~1023 bits, and isPrime(d) must be true
        # Let's search more carefully
        
        # Alternative: use the relationship
        # e*d = phi + s (s = ±1) with t=1
        # e*d - s = (p^k - 1)(q^k - 1)
        #
        # Let phi = (p^k - 1)(q^k - 1)
        # We want to find d such that:
        # 1) d is prime
        # 2) d has about 1023-1024 bits
        # 3) (e*d - s) = phi = (p^k-1)(q^k-1) for some valid p,q with p*q=N
        
        # From e*d = phi + s, we get d = (phi + s) / e
        # We need to find the correct phi
        
        # phi = (p^k-1)(q^k-1) where p*q = N
        # For each k, there's only one valid phi (once we know p,q)
        
        # But we're trying to find p,q! Chicken and egg...
        # 
        # Key insight: phi ≈ N^k when k ≤ 2, or more precisely:
        # phi = N^k - (p^k + q^k) + 1
        # 
        # For k=2: phi = N^2 - (p^2 + q^2) + 1
        # p^2 + q^2 = (p+q)^2 - 2pq = (p+q)^2 - 2N
        # 
        # Let s = p + q (unknown but p+q ≈ 2*sqrt(N))
        # phi = N^2 - s^2 + 2N + 1 = N^2 + 2N + 1 - s^2 = (N+1)^2 - s^2
        
        if k == 2:
            print("  [*] Using special approach for k=2")
            # phi = (N+1)^2 - (p+q)^2
            # e*d = phi ± 1
            # e*d = (N+1)^2 - (p+q)^2 ± 1
            # 
            # Let S = p + q
            # S^2 = (N+1)^2 - e*d ∓ 1
            #
            # For this to work, (N+1)^2 - e*d ∓ 1 must be a perfect square
            # and S^2 - 4N must be a perfect square (discriminant for finding p,q)
            
            # We don't know d, but d ≈ N with high bits
            # Let's try: for various d values, check if we get valid factors
            
            # Actually, simpler approach:
            # d is prime with ~1023 bits
            # e*d ≈ (N+1)^2 since phi ≈ N^2 for k=2
            # So d ≈ (N+1)^2 / e
            
            d_estimate = ((N+1)**2) // e
            print(f"  [*] d estimate: {d_estimate.bit_length()} bits")
            print(f"  [*] d estimate: {d_estimate}")
            
            # Search around this estimate
            for delta in range(-100000, 100001):
                d_try = d_estimate + delta
                if d_try <= 0:
                    continue
                    
                for s in [1, -1]:
                    # phi = e*d - s
                    phi_try = e * d_try - s
                    
                    # For k=2: phi = (N+1)^2 - S^2 where S = p+q
                    # S^2 = (N+1)^2 - phi = (N+1)^2 - e*d + s
                    
                    S_squared = (N+1)**2 - phi_try
                    if S_squared <= 0:
                        continue
                    
                    S = isqrt(S_squared)
                    if S * S != S_squared:
                        continue
                    
                    # Now we have S = p + q
                    # p*q = N
                    # p and q are roots of: x^2 - Sx + N = 0
                    disc = S*S - 4*N
                    if disc < 0:
                        continue
                    
                    sqrt_disc = isqrt(disc)
                    if sqrt_disc * sqrt_disc != disc:
                        continue
                    
                    p = (S + sqrt_disc) // 2
                    q = (S - sqrt_disc) // 2
                    
                    if p * q == N:
                        print(f"  [+] Found! delta={delta}, s={s}")
                        print(f"      p = {p}")
                        print(f"      q = {q}")
                        print(f"      d = {d_try}")
                        return p, q, d_try, k
    
    return None

# Test with provided values
N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("[*] Starting attack...")
result = attack(N, e)
print(f"\n[*] Result: {result}")
