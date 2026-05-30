#!/usr/bin/env python3
"""
Kiss ASIS - Attack using Continued Fractions
The key relationship: e*d ≡ ±1 (mod phi) where phi = (p^k - 1)(q^k - 1)
With d ≈ N and k=3, we have e ≈ N^2 and phi ≈ N^3
So e/phi ≈ 1/d, meaning continued fractions of e/phi approximates d

But we don't know phi! However, phi ≈ N^k, so we can use e/N^k
"""

from Crypto.Util.number import *
from math import gcd, isqrt
from fractions import Fraction

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

def continued_fraction(num, den, max_terms=500):
    """Compute continued fraction expansion of num/den"""
    cf = []
    while den and len(cf) < max_terms:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf

def convergents(cf):
    """Compute convergents from continued fraction"""
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    for a in cf:
        h_prev, h_curr = h_curr, a * h_curr + h_prev
        k_prev, k_curr = k_curr, a * k_curr + k_prev
        yield h_curr, k_curr

def solve_for_k2(N, phi):
    """
    For k=2: phi = (p^2-1)(q^2-1) = (N+1)^2 - S^2 where S = p+q
    Returns p, q if found
    """
    S_sq = (N+1)**2 - phi
    if S_sq <= 0:
        return None, None
    S = isqrt(S_sq)
    if S * S != S_sq:
        return None, None
    
    # p + q = S, p * q = N
    disc = S*S - 4*N
    if disc < 0:
        return None, None
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None, None
    
    p = (S + sqrt_disc) // 2
    q = (S - sqrt_disc) // 2
    if p * q == N:
        return p, q
    return None, None

def solve_for_k3(N, phi):
    """
    For k=3: phi = (p^3-1)(q^3-1) = N^3 - S^3 + 3NS + 1 where S = p+q
    Returns p, q if found
    """
    # S^3 - 3*N*S = N^3 + 1 - phi
    RHS = N**3 + 1 - phi
    
    # Solve cubic using Newton-Raphson
    S = 2 * isqrt(N)
    
    for _ in range(200):
        f = S**3 - 3*N*S - RHS
        fp = 3*S**2 - 3*N
        if fp == 0:
            break
        delta = f // fp
        if delta == 0:
            break
        S = S - delta
    
    # Check nearby values
    for delta in range(-5, 6):
        SS = S + delta
        if SS > 0 and SS**3 - 3*N*SS == RHS:
            # Found S!
            disc = SS*SS - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            p = (SS + sqrt_disc) // 2
            q = (SS - sqrt_disc) // 2
            if p * q == N:
                return p, q
    
    return None, None

def solve_for_k(N, phi, k):
    """General solver for any k"""
    if k == 2:
        return solve_for_k2(N, phi)
    elif k == 3:
        return solve_for_k3(N, phi)
    else:
        # For k >= 4, use numerical methods
        # phi = (p^k - 1)(q^k - 1) = N^k - (p^k + q^k) + 1
        # This is more complex, skip for now
        return None, None

def attack(N, e):
    """Main attack using continued fractions"""
    print("\n[*] Starting continued fraction attack...")
    
    for k in [2, 3, 4]:  # Most likely k values based on e size
        print(f"\n[*] Trying k = {k}")
        Nk = N ** k
        
        # Compute continued fraction of e / N^k
        cf = continued_fraction(e, Nk)
        print(f"    CF has {len(cf)} terms")
        
        # Check each convergent
        for i, (h, k_conv) in enumerate(convergents(cf)):
            # h/k is an approximation to e/N^k
            # Since e*d ≈ phi ≈ N^k, we have e/N^k ≈ 1/d
            # So k_conv might be close to d
            
            d_candidate = k_conv
            
            # Check if d_candidate has reasonable bit size (around 1023)
            if not (1015 <= d_candidate.bit_length() <= 1030):
                continue
            
            # For each T and sign, compute phi and try to factor
            for T in range(1, 10):
                for sign in [1, -1]:
                    phi_times_T = e * d_candidate - sign
                    if phi_times_T <= 0 or phi_times_T % T != 0:
                        continue
                    phi = phi_times_T // T
                    
                    p, q = solve_for_k(N, phi, k)
                    if p and q:
                        print(f"\n[+] FOUND!")
                        print(f"    k = {k}")
                        print(f"    T = {T}")
                        print(f"    sign = {sign}")
                        print(f"    d = {d_candidate}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        return p, q, d_candidate, k, T, sign
        
        # Also try h as potential d (the other fraction component)
        for i, (h, k_conv) in enumerate(convergents(cf)):
            d_candidate = h
            
            if not (1015 <= d_candidate.bit_length() <= 1030):
                continue
            
            for T in range(1, 10):
                for sign in [1, -1]:
                    phi_times_T = e * d_candidate - sign
                    if phi_times_T <= 0 or phi_times_T % T != 0:
                        continue
                    phi = phi_times_T // T
                    
                    p, q = solve_for_k(N, phi, k)
                    if p and q:
                        print(f"\n[+] FOUND!")
                        print(f"    k = {k}")
                        print(f"    T = {T}")
                        print(f"    sign = {sign}")
                        print(f"    d = {d_candidate}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        return p, q, d_candidate, k, T, sign
    
    return None

# Alternative approach: Direct search using the relationship
def direct_attack(N, e):
    """
    Direct attack: since e ≈ N^(k-1) and d ≈ N,
    we have e*d ≈ N^k ≈ phi
    
    For each k, compute d ≈ N^k / e and search around it
    """
    print("\n[*] Starting direct attack...")
    
    for k in [2, 3]:
        print(f"\n[*] Trying k = {k}")
        Nk = N ** k
        
        for T in range(1, 20):
            for sign in [1, -1]:
                # e*d = T*phi + sign
                # d = (T*phi + sign) / e
                # phi ≈ N^k, so d ≈ (T*N^k + sign) / e
                
                d_base = (T * Nk) // e
                
                # Search around d_base
                for delta in range(-1000, 1001):
                    d = d_base + delta
                    if d <= 0:
                        continue
                    
                    phi_times_T = e * d - sign
                    if phi_times_T <= 0 or phi_times_T % T != 0:
                        continue
                    
                    phi = phi_times_T // T
                    
                    p, q = solve_for_k(N, phi, k)
                    if p and q:
                        print(f"\n[+] FOUND!")
                        print(f"    k = {k}")
                        print(f"    T = {T}")
                        print(f"    sign = {sign}")
                        print(f"    delta = {delta}")
                        print(f"    d = {d}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        return p, q, d, k, T, sign
    
    return None

# Run the attacks
result = attack(N, e)
if result is None:
    print("\n[*] CF attack failed, trying direct attack...")
    result = direct_attack(N, e)

if result:
    p, q, d, k, T, sign = result
    print("\n" + "="*60)
    print("SUCCESS!")
    print("="*60)
    
    # Verify by decrypting
    phi = (p**k - 1) * (q**k - 1)
    
    # Compute proper d from phi
    for r in [0, 1]:
        try:
            d_real = inverse((-1)**r, phi) * e % phi
            d_real = inverse(e, phi) if r == 0 else (phi - inverse(e, phi)) % phi
            m = pow(enc, d_real, N)
            msg = long_to_bytes(m)
            try:
                msg_str = msg.decode('latin-1')
                if all(32 <= ord(c) <= 126 for c in msg_str):
                    print(f"Decrypted message: {msg_str}")
            except:
                pass
        except:
            pass
else:
    print("\n[-] Attack failed!")
