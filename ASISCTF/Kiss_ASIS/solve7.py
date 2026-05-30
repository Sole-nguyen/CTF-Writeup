#!/usr/bin/env python3
"""
Kiss ASIS - Using SageMath for Coppersmith/Lattice attack

The key insight: e * d === +/-1 (mod phi) where phi = (p^k - 1)(q^k - 1)
With d being a large prime (~1023 bits) and e known,
we can set up a lattice problem.

For k=3 and t=1:
e * d = phi + r where r = +/-1
e * d = (p^3 - 1)(q^3 - 1) + r

Let's try to find the relationship more directly.
"""

import subprocess
import sys

# Create a SageMath script
sage_script = '''
# Kiss ASIS solver using SageMath

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.nbits()}")
print(f"e bits: {e.nbits()}")

# Try Wiener's attack variant for large d
# When d is large, we need the "inverse" Wiener attack

# For e*d = k*phi + 1:
# e/phi = k/d + 1/(d*phi)
# So k/d approximates e/phi

# For k=2: phi = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)
# We can approximate phi ≈ N^2

# But the standard approach might not work. Let's try Boneh-Durfee.

def boneh_durfee(N, e, k_approx=2, delta=0.27, m=4):
    """
    Boneh-Durfee attack for large d
    Works when d < N^(0.292)
    
    But in this case, d ≈ N, so this won't work directly.
    """
    print("Standard Boneh-Durfee won't work for d ≈ N")
    return None

# Alternative: If we know k, we can set up equations
# e * d ≡ ±1 (mod phi)
# phi = (p^k - 1)(q^k - 1)

# For k=2:
# phi = (p-1)(p+1)(q-1)(q+1) = (N - (p+q) + 1)(N + (p+q) + 1) = N^2 + 2N + 1 - (p+q)^2

# Let S = p + q. Then:
# phi = (N+1)^2 - S^2

# e * d === +/-1 (mod phi)
# e * d = t * phi +/- 1 for some t

# If we can find t, d such that (e*d -/+ 1) / t = (N+1)^2 - S^2 for some valid S

# This requires guessing t. For small t:
for k in [2, 3, 1]:
    print(f"\\nTrying k = {k}")
    
    if k == 2:
        # For k=2, phi = (N+1)^2 - S^2
        # e*d = t*phi + r
        # We need to find t, d, and S
        
        for t in range(1, 100):
            # e*d = t * ((N+1)^2 - S^2) + r
            # We don't know d or S...
            
            # But! e*d is approximately t * N^2
            # So d is approximately t * N^2 / e
            
            d_approx = (t * N^2) // e
            
            for delta in range(-10, 11):
                d = d_approx + delta
                if d <= 0:
                    continue
                
                for r in [1, -1]:
                    val = e * d - r
                    if val <= 0 or val % t != 0:
                        continue
                    
                    phi = val // t
                    
                    # Check if phi = (N+1)^2 - S^2 for some integer S
                    S_sq = (N+1)^2 - phi
                    if S_sq <= 0:
                        continue
                    
                    S = isqrt(S_sq)
                    if S * S != S_sq:
                        continue
                    
                    # Found S! Now find p, q
                    # p + q = S, p * q = N
                    disc = S*S - 4*N
                    if disc < 0:
                        continue
                    sqrt_disc = isqrt(disc)
                    if sqrt_disc * sqrt_disc != disc:
                        continue
                    
                    p = (S + sqrt_disc) // 2
                    q = (S - sqrt_disc) // 2
                    
                    if p * q == N:
                        print(f"FOUND! k={k}, t={t}, r={r}")
                        print(f"p = {p}")
                        print(f"q = {q}")
                        
                        # Verify and decrypt
                        phi_check = (p^2 - 1) * (q^2 - 1)
                        print(f"phi matches: {phi == phi_check}")
                        
                        d_real = inverse_mod(e, phi_check)
                        m = power_mod(enc, d_real, N)
                        msg = int(m).to_bytes((int(m).bit_length() + 7) // 8, 'big')
                        print(f"Decrypted: {msg}")
                        exit(0)

print("\\nNo solution found with simple search")
'''

# Write and run Sage script
with open('solve_sage.sage', 'w') as f:
    f.write(sage_script)

print("Created solve_sage.sage")
print("To run: sage solve_sage.sage")
print("Or if Sage is not installed, we need to use pure Python")

# Pure Python fallback with expanded search
print("\n" + "="*60)
print("Running pure Python expanded search...")
print("="*60)

from Crypto.Util.number import *
from math import isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

def search_k2():
    """Search for k=2 with larger t range"""
    print("\nSearching for k=2...")
    N2 = N * N
    
    for t in range(1, 10000):
        if t % 1000 == 0:
            print(f"  t = {t}...")
        
        # d is approximately t * N^2 / e
        d_approx = (t * N2) // e
        
        for delta in range(-50, 51):
            d = d_approx + delta
            if d <= 0:
                continue
            
            for r in [1, -1]:
                val = e * d - r
                if val <= 0 or val % t != 0:
                    continue
                
                phi = val // t
                
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
                    print(f"\n[+] FOUND! k=2, t={t}, r={r}")
                    print(f"    p = {p}")
                    print(f"    q = {q}")
                    return p, q
    
    return None, None

def search_k3():
    """Search for k=3 with larger t range"""
    print("\nSearching for k=3...")
    N3 = N ** 3
    
    for t in range(1, 5000):
        if t % 500 == 0:
            print(f"  t = {t}...")
        
        d_approx = (t * N3) // e
        
        for delta in range(-50, 51):
            d = d_approx + delta
            if d <= 0:
                continue
            
            for r in [1, -1]:
                val = e * d - r
                if val <= 0 or val % t != 0:
                    continue
                
                phi = val // t
                
                # For k=3: S^3 - 3NS = N^3 + 1 - phi
                RHS = N**3 + 1 - phi
                
                # Solve cubic
                S = 2 * isqrt(N)
                for _ in range(200):
                    f = S**3 - 3*N*S - RHS
                    fp = 3*S*S - 3*N
                    if fp == 0:
                        break
                    S_new = S - f // fp
                    if abs(S_new - S) <= 1:
                        break
                    S = S_new
                
                # Check nearby
                found = False
                for ds in range(-20, 21):
                    SS = S + ds
                    if SS <= 0:
                        continue
                    if SS**3 - 3*N*SS == RHS:
                        disc = SS*SS - 4*N
                        if disc < 0:
                            continue
                        sqrt_disc = isqrt(disc)
                        if sqrt_disc * sqrt_disc != disc:
                            continue
                        p = (SS + sqrt_disc) // 2
                        q = (SS - sqrt_disc) // 2
                        if p * q == N and isPrime(p) and isPrime(q):
                            print(f"\n[+] FOUND! k=3, t={t}, r={r}")
                            print(f"    p = {p}")
                            print(f"    q = {q}")
                            return p, q
    
    return None, None

# Run searches
p, q = search_k2()
if p is None:
    p, q = search_k3()

if p:
    print("\nSuccess! Decrypting...")
    for k in [2, 3]:
        try:
            phi = (p**k - 1) * (q**k - 1)
            d = inverse(e, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            print(f"k={k}: {msg}")
        except:
            pass
else:
    print("\nFailed to find factors.")
