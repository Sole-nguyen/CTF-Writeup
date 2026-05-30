#!/usr/bin/env python3
"""
Kiss ASIS - Final Solver
Key insight: e is computed as inverse(phi ± d, phi)
When e is very large (close to phi), it means (phi ± d) is small relative to phi.

For k=1: phi ≈ N, d ≈ 0.999*N
So phi - d or phi + d could tell us about p and q

e = inverse(phi ± d, phi) 
e * (phi ± d) ≡ 1 (mod phi)
e * (phi ± d) = m * phi + 1

Since e ≈ phi, and (phi ± d) ≈ phi ± 0.999*N:
- For +d: phi + d ≈ 2*phi (if d ≈ phi)
- For -d: phi - d ≈ 0.001*phi (if d ≈ 0.999*phi)

The second case is interesting: if phi - d is very small,
then e ≈ phi / (phi - d) would be very large!
"""

from Crypto.Util.number import *
from math import gcd, isqrt
from sympy import factorint

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

# From the code:
# e = inverse(phi + (-1)^r * d, phi)
# where phi = (p^k - 1)(q^k - 1) and k ∈ [1,6]

# e * (phi ± d) ≡ 1 (mod phi)
# e * (phi ± d) = m * phi + 1 for some m ≥ 1

# Rearranging:
# e * phi ± e * d = m * phi + 1
# ± e * d = (m - e) * phi + 1

# Let A = m - e
# ± e * d = A * phi + 1

# Case 1: +e*d = A*phi + 1
# e*d - 1 = A * phi
# 
# Case 2: -e*d = A*phi + 1
# e*d + 1 = -A * phi

# Since e*d > 0 and phi > 0:
# Case 1: A = (e*d - 1) / phi > 0 if e*d > phi
# Case 2: -A = (e*d + 1) / phi, so A < 0

# For k=1: phi ≈ N, d ≈ 0.999N, e ≈ N^2 (from observation)
# e*d ≈ N^2 * N = N^3
# A ≈ N^3 / N = N^2 (huge!)

# So for k=1, A is very large, meaning m = e + A ≈ e + N^2 ≈ 2*N^2

# For k=2: phi ≈ N^2, d ≈ N, e ≈ ?
# We observed e ≈ 0.78 * N^2
# e*d ≈ 0.78 * N^2 * N = 0.78 * N^3
# A ≈ 0.78 * N^3 / N^2 = 0.78 * N

# Hmm, A is still large...

# Wait, let me reconsider. The equation was:
# e * (phi ± d) = m * phi + 1
# 
# If e ≈ phi (which is true for k=2 since e ≈ 0.78*N² and phi ≈ N²):
# phi * (phi ± d) ≈ m * phi + 1
# phi ± d ≈ m + 1/phi
# m ≈ phi ± d

# So m ≈ phi ± d, which for k=2 means m ≈ N² ± N ≈ N²

# The relationship I should exploit:
# e * (phi + (-1)^r * d) = m * phi + 1
# 
# Let X = phi + (-1)^r * d
# e * X = m * phi + 1
# e * X ≡ 1 (mod phi)
# 
# So X = inverse(e, phi)!

# But we don't know phi... unless we can figure out X first.

# Key observation: X = phi ± d
# For k=2: phi = (p²-1)(q²-1), d ≈ N
# X = phi ± d = (p²-1)(q²-1) ± d

# X can be estimated from e:
# e = inverse(X, phi)
# e * X ≡ 1 (mod phi)
# e * X = m * phi + 1

# Since e ≈ phi, we have:
# phi * X ≈ m * phi + 1
# X ≈ m + 1/phi ≈ m (for large phi)

# So X ≈ m. But what is m?

# From e * X = m * phi + 1:
# m = (e * X - 1) / phi

# Since e ≈ phi and X ≈ m, we get:
# m ≈ (phi * m - 1) / phi = m - 1/phi ≈ m

# This is circular. Let me try numerical approach.

# For k=2, estimate:
# phi ≈ N² = 4.438... × 10^615 (approximately)
# e ≈ 0.78 * N² ≈ 3.44 × 10^615
# d ≈ N ≈ 6.66 × 10^307

# X = phi + d or X = phi - d
# X ≈ N² ± N ≈ N² (since N << N²)

# e * X ≈ 0.78 * N² * N² = 0.78 * N^4
# m * phi ≈ m * N²
# So m ≈ 0.78 * N^4 / N² = 0.78 * N²

# m ≈ e! This makes sense since e * X = m * phi + 1 and X ≈ phi implies m ≈ e.

# Now the key question: can we determine X more precisely?

# We know: e * X = m * phi + 1
# And: X = phi ± d

# Substituting:
# e * (phi ± d) = m * phi + 1
# e * phi ± e * d = m * phi + 1
# (e - m) * phi = 1 ∓ e * d
# 
# Let B = e - m
# B * phi = 1 ∓ e * d

# If r=1 (so X = phi - d):
# B * phi = 1 + e * d  ... (eq1)

# If r=0 (so X = phi + d):
# B * phi = 1 - e * d  ... (eq2)

# For eq2: B * phi = 1 - e*d < 0 (since e*d >> 1)
# So B < 0, meaning m > e.

# For eq1: B * phi = 1 + e*d > 0
# So B > 0, meaning m < e.

# Given that e ≈ phi, if m < e, then m could be significantly less than e.
# B = e - m could be relatively small!

# This is the key insight: B = e - m could be small!

# From eq1: B * phi = e*d + 1
# B = (e*d + 1) / phi

# For k=2: B ≈ (0.78*N² * N) / N² = 0.78*N

# B has about N bits (1023 bits), which is large but manageable.

# Now, we can use:
# e - m = B
# e * X = m * phi + 1 = (e - B) * phi + 1
# e * X - e * phi = -B * phi + 1
# e * (X - phi) = -B * phi + 1
# 
# Since X = phi - d (assuming r=1):
# e * (-d) = -B * phi + 1
# e * d = B * phi - 1
# 
# This gives us: e * d + 1 = B * phi  ... same as eq1

# The question is: how to find B and d such that this equation holds
# and phi = (p^k - 1)(q^k - 1) for some valid p, q with p*q = N?

# Continued fraction approach:
# e * d + 1 = B * phi
# e / phi = B / d - 1/(d*phi)
# e / phi ≈ B / d

# So B/d is a convergent of e/phi!
# But we don't know phi exactly. We can approximate phi ≈ N^k.

print("\n" + "="*60)
print("Trying approximation phi ≈ N^k and using continued fractions")
print("="*60)

def get_convergents(num, den):
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    a, b = num, den
    while b:
        q = a // b
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        yield (h_curr, k_curr)
        a, b = b, a % b

def factor_from_phi(N, phi, k):
    """Given phi = (p^k - 1)(q^k - 1), find p, q"""
    if k == 1:
        # phi = (p-1)(q-1) = N - p - q + 1
        # p + q = N + 1 - phi
        S = N + 1 - phi
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
    
    elif k == 2:
        # phi = (p²-1)(q²-1) = (N+1)² - (p+q)²
        # (p+q)² = (N+1)² - phi
        S_sq = (N+1)**2 - phi
        if S_sq <= 0:
            return None, None
        S = isqrt(S_sq)
        if S*S != S_sq:
            return None, None
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
    
    elif k == 3:
        # phi = (p³-1)(q³-1) = N³ - (p³+q³) + 1
        # p³ + q³ = (p+q)³ - 3pq(p+q) = S³ - 3NS
        # phi = N³ - S³ + 3NS + 1
        # S³ - 3NS = N³ + 1 - phi
        RHS = N**3 + 1 - phi
        
        # Newton-Raphson for S
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
        for delta in range(-10, 11):
            SS = S + delta
            if SS > 0 and SS**3 - 3*N*SS == RHS:
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
    
    return None, None

# Try each k
for k in [2, 1, 3]:
    print(f"\n[*] Trying k = {k}")
    phi_approx = N ** k
    
    # Get convergents of e / phi_approx
    conv_count = 0
    for B, d in get_convergents(e, phi_approx):
        conv_count += 1
        if conv_count > 500:
            break
        
        # Check if d is in the right range (about 1023 bits)
        if not (1018 <= d.bit_length() <= 1028):
            continue
        
        # From e*d + 1 = B*phi (for r=1)
        # phi = (e*d + 1) / B
        
        # Or from e*d - 1 = B*phi (for r=0)
        # phi = (e*d - 1) / B
        
        for sign in [1, -1]:
            val = e * d + sign
            if val % B != 0:
                continue
            phi = val // B
            
            p, q = factor_from_phi(N, phi, k)
            if p and q:
                print(f"\n[+] FOUND!")
                print(f"    k = {k}")
                print(f"    B = {B}")
                print(f"    d = {d}")
                print(f"    sign = {sign}")
                print(f"    phi = {phi}")
                print(f"    p = {p}")
                print(f"    q = {q}")
                
                # Verify
                phi_real = (p**k - 1) * (q**k - 1)
                print(f"    phi_real = {phi_real}")
                print(f"    phi match: {phi == phi_real}")
                
                # Decrypt
                d_real = inverse(e, phi_real)
                m = pow(enc, d_real, N)
                msg = long_to_bytes(m)
                print(f"    Decrypted: {msg}")
                exit(0)

print("\n[-] Not found with continued fractions approach")

# Alternative: brute force small B values
print("\n[*] Trying brute force for small B values...")

for k in [2, 1]:
    print(f"\n[*] Trying k = {k}")
    
    for B in range(1, 10000):
        if B % 1000 == 0:
            print(f"    B = {B}...")
        
        for sign in [1, -1]:
            # e*d + sign = B * phi
            # We need to find d and phi such that:
            # 1) d is about 1023 bits
            # 2) phi = (p^k - 1)(q^k - 1) for p*q = N
            
            # From phi ≈ N^k:
            # e*d ≈ B * N^k - sign
            # d ≈ (B * N^k - sign) / e
            
            d_approx = (B * (N**k) - sign) // e
            
            if d_approx <= 0:
                continue
            
            # Check nearby d values
            for delta in range(-3, 4):
                d = d_approx + delta
                if d <= 0:
                    continue
                
                val = e * d + sign
                if val % B != 0:
                    continue
                
                phi = val // B
                
                p, q = factor_from_phi(N, phi, k)
                if p and q:
                    print(f"\n[+] FOUND!")
                    print(f"    k = {k}")
                    print(f"    B = {B}")
                    print(f"    d = {d}")
                    print(f"    sign = {sign}")
                    print(f"    p = {p}")
                    print(f"    q = {q}")
                    
                    # Decrypt
                    phi_real = (p**k - 1) * (q**k - 1)
                    d_real = inverse(e, phi_real)
                    m = pow(enc, d_real, N)
                    msg = long_to_bytes(m)
                    print(f"    Decrypted: {msg}")
                    exit(0)

print("\n[-] Attack failed")
