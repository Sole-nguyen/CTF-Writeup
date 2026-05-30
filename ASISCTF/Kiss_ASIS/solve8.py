#!/usr/bin/env python3
"""
Kiss ASIS - Expanded Search
"""

from Crypto.Util.number import *
from math import isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

def search_k2():
    """Search for k=2 with larger t range"""
    print("\nSearching for k=2...")
    N2 = N * N
    
    for t in range(1, 10000):
        if t % 1000 == 0:
            print(f"  t = {t}...")
        
        # d approx t * N^2 / e
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

def search_k1():
    """Search for k=1"""
    print("\nSearching for k=1...")
    
    for t in range(1, 100000):
        if t % 10000 == 0:
            print(f"  t = {t}...")
        
        d_approx = (t * N) // e
        
        for delta in range(-100, 101):
            d = d_approx + delta
            if d <= 0:
                continue
            
            for r in [1, -1]:
                val = e * d - r
                if val <= 0 or val % t != 0:
                    continue
                
                phi = val // t
                
                # For k=1: phi = (p-1)(q-1) = N - p - q + 1
                # p + q = N + 1 - phi
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
                
                if p * q == N:
                    print(f"\n[+] FOUND! k=1, t={t}, r={r}")
                    print(f"    p = {p}")
                    print(f"    q = {q}")
                    return p, q
    
    return None, None

# Run searches
print("="*60)
print("Running expanded search...")
print("="*60)

p, q = search_k2()
if p is None:
    p, q = search_k3()
if p is None:
    p, q = search_k1()

if p:
    print("\nSuccess! Decrypting...")
    for k in [1, 2, 3, 4, 5, 6]:
        try:
            phi = (p**k - 1) * (q**k - 1)
            d = inverse(e, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            if all(32 <= b <= 126 for b in msg):
                print(f"k={k}: {msg}")
        except:
            pass
else:
    print("\nFailed to find factors.")
