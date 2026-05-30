#!/usr/bin/env python3
"""
Kiss ASIS - Deep Analysis
Let's carefully analyze the relationship between e, d, N, and phi
"""

from Crypto.Util.number import *
from math import gcd, isqrt

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N = {N}")
print(f"N bits: {N.bit_length()}")
print(f"\ne = {e}")
print(f"e bits: {e.bit_length()}")

# Key insight: Look at e more carefully
# e = inverse(phi + (-1)^r * d, phi)
# This means e * (phi + (-1)^r * d) ≡ 1 (mod phi)
# => e * phi + e * (-1)^r * d ≡ 1 (mod phi)
# => e * (-1)^r * d ≡ 1 (mod phi)
# 
# So e * d ≡ (-1)^r (mod phi), meaning e * d = k * phi + (-1)^r for some k

# Notice: e is larger than N^2!
# e has 2045 bits, N has 1023 bits, N^2 has 2046 bits
# So e < N^2 (just barely)

print(f"\nN^2 bits: {(N*N).bit_length()}")
print(f"e < N^2: {e < N*N}")
print(f"e / N^2 = {e * 10**10 // (N*N) / 10**10}")

# If e < N^2, then for k=2:
# phi = (p^2-1)(q^2-1) ≈ N^2
# e < phi, so e could be a valid public exponent for standard RSA with this phi

# But wait, the code says:
# e = inverse(phi + (-1)**r * d, phi)
# where phi = (p^k - 1)(q^k - 1)
#
# For this inverse to exist and be meaningful:
# - gcd(phi + (-1)^r * d, phi) = 1
# - This is equivalent to gcd(d, phi) = 1 (since (-1)^r * d is just ±d)
# - Since d is a large prime, this is almost always true

# Let's think about the sizes again:
# - N = 1024 bits
# - d = 1024 * 0.999 ≈ 1023 bits (d is prime)
# - phi = (p^k - 1)(q^k - 1)
#
# For k=1: phi ≈ N (1024 bits)
# For k=2: phi ≈ N^2 (2046 bits)
# For k=3: phi ≈ N^3 (3069 bits)

# Now, e = inverse(phi ± d, phi)
# e * (phi ± d) ≡ 1 (mod phi)
# e * (phi ± d) = m * phi + 1 for some positive integer m
# e ≈ (m * phi) / (phi ± d)

# If phi >> d, then phi ± d ≈ phi, so e ≈ m
# If phi ≈ d, then phi ± d ≈ 2*d or 0, and e would be large or undefined

# For k=2: phi ≈ N^2 ≈ 2046 bits, d ≈ 1023 bits
# phi >> d, so e ≈ m (where m = (e * (phi ± d) - 1) / phi)

# But we see e has 2045 bits, close to phi!
# This means m ≈ e (approximately), which is huge.

# Let me reconsider...
# e * (phi ± d) = m * phi + 1
# e * phi ± e * d = m * phi + 1
# (e - m) * phi = 1 ∓ e * d
# If e ≈ phi (same bit length), then:
# (e - m) * phi = 1 ∓ e * d
# 
# For this to work: e ≈ m, so (e - m) is small
# Then (e - m) * phi ≈ 1 ∓ e * d
# e * d ≈ (m - e) * phi - 1

# Let Δ = m - e (could be positive or negative, but small in magnitude)
# e * d ≈ Δ * phi ± 1

# This is the key! Δ = m - e should be small!

# Since e = inverse(phi ± d, phi), we have:
# e * (phi ± d) ≡ 1 (mod phi)
# e * (phi ± d) = m * phi + 1
# e = (m * phi + 1) / (phi ± d)
# 
# If r = 0: e = (m * phi + 1) / (phi + d)
# If r = 1: e = (m * phi + 1) / (phi - d)

# For r = 1 (phi - d case):
# If d is close to phi, then phi - d is small!
# e = (m * phi + 1) / (phi - d)
# If phi - d is small, e can be very large!

# Given e ≈ N^2 and phi ≈ N^2 for k=2, and d ≈ N:
# phi - d ≈ N^2 - N ≈ N^2 (still large)

# Hmm, but for k=1:
# phi ≈ N, d ≈ N
# phi - d could be small if d ≈ phi!

# Wait, d has about 1023 bits and for k=1, phi = (p-1)(q-1) also has about 1023 bits
# So d ≈ phi is possible!

# In that case:
# e = (m * phi + 1) / (phi - d)
# If phi ≈ d, then phi - d is very small
# And e would be huge, proportional to phi / (phi - d)

# Let's check: for k=1, phi ≈ N
# If d ≈ phi ≈ N, then phi - d could be as small as 1
# And e ≈ phi * m / 1 ≈ N * m

# Given e ≈ N^2, this means m ≈ N
# So e * (phi - d) ≈ m * phi
# e ≈ m * phi / (phi - d)

# If phi - d ≈ 1, then e ≈ m * N ≈ N^2, which matches!

print("\n" + "="*60)
print("Key insight: k=1 with d ≈ phi (Boneh-Durfee regime)")
print("="*60)

# For k=1:
# phi = (p-1)(q-1)
# e * d ≡ ±1 (mod phi)
# But now, d ≈ phi!

# The attack:
# e * d = t * phi ± 1
# With d ≈ phi (both about N bits) and e ≈ N^2:
# e * d ≈ N^2 * N = N^3
# t * phi ≈ N^3
# t ≈ N^2

# This doesn't give us small t...

# Let me try yet another approach.
# Consider: e = inverse(phi - d, phi) when r=1
# e * (phi - d) ≡ 1 (mod phi)
# e * (phi - d) = m * phi + 1

# Let X = phi - d (could be small since d ≈ phi for k=1)
# e * X = m * phi + 1

# If X is small (say, X has b bits where b << 1024):
# e * X = m * phi + 1
# Since e ≈ N^2 and phi ≈ N:
# N^2 * X ≈ m * N
# m ≈ N * X

# For this to give us something useful, we need to know X
# But X = phi - d, and we don't know phi or d!

# However, we can use:
# e * (phi - d) = m * phi + 1
# e * phi - e * d = m * phi + 1
# (e - m) * phi = e * d + 1

# Let A = e - m
# A * phi = e * d + 1

# For k=1: phi ≈ N, d ≈ N, e ≈ N^2
# A * N ≈ N^2 * N = N^3
# A ≈ N^2 ≈ e

# So m ≈ e - N^2 ≈ 0 (or small)!

# That means:
# m * phi ≈ 0
# e * (phi - d) ≈ 1

# So phi - d ≈ 1/e, which is basically 0
# Meaning d ≈ phi for k=1!

print("\nCritical observation: d ≈ phi for k=1")
print("This means: phi - d is very small!")

# If d ≈ phi = (p-1)(q-1), and d is prime:
# d ≈ (p-1)(q-1)

# Let's use the equation:
# e * (phi - d) = m * phi + 1
# If m is small (m ≈ 1), then:
# e * (phi - d) ≈ phi + 1
# phi - d ≈ (phi + 1) / e

# For the example:
# phi ≈ N ≈ 10^307
# e ≈ N^2 ≈ 10^614
# (phi + 1) / e ≈ N / N^2 = 1/N ≈ 10^-307

# This means phi - d ≈ 0, so d ≈ phi

# But we need an exact relationship!

# Key equation: e * (phi - d) = m * phi + 1
# Rearranging: e * phi - e * d = m * phi + 1
# e * d = (e - m) * phi - 1

# Let's denote e - m = k (some integer)
# e * d = k * phi - 1

# From e * (phi - d) = m * phi + 1:
# m = (e * (phi - d) - 1) / phi = e - e*d/phi - 1/phi ≈ e - e*d/phi

# Since e*d ≈ k*phi for some k, we have m ≈ e - k

# GCD approach:
# gcd(e, N) should give us information
g = gcd(e, N)
print(f"\ngcd(e, N) = {g}")

# Continued fractions on e/N:
print("\nTrying continued fractions on e/N...")

def cf_expansion(num, den, max_terms=100):
    cf = []
    while den and len(cf) < max_terms:
        q = num // den
        cf.append(q)
        num, den = den, num % q * den if q else 0
        num, den = den, num % den if den else 0
    return cf

def get_convergents(num, den, max_terms=100):
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    a, b = num, den
    results = []
    term = 0
    while b and term < max_terms:
        q = a // b
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        results.append((h_curr, k_curr, q))
        a, b = b, a % b
        term += 1
    return results

convs = get_convergents(e, N, 200)
print(f"Got {len(convs)} convergents")

# For Wiener attack variant:
# If e*d ≡ 1 (mod phi) and d is small, then k/d ≈ e/phi where k*phi = e*d - 1
# But here d is large (≈ phi), so we need inverse approach

# Actually, for large d:
# e*d = k*phi + 1
# e/phi = k/d + 1/(d*phi)
# e/phi ≈ k/d

# So k/d is a convergent of e/phi
# But phi = (p-1)(q-1) ≈ N - p - q + 1

# Estimate phi ≈ N (ignoring the small p+q term):
# e/N ≈ k/d

# Check convergents:
for i, (h, k, q) in enumerate(convs[:50]):
    # h/k ≈ e/N
    # So if this is k_real/d_real, then h = k_real, k = d_real
    
    # Let's assume d = k (the denominator of convergent)
    d_guess = k
    
    if d_guess.bit_length() < 1010 or d_guess.bit_length() > 1030:
        continue
    
    print(f"\nConvergent {i}: h/k bits = {h.bit_length()}/{k.bit_length()}")
    
    # Check if d_guess works
    # e*d ≡ ±1 (mod phi) where phi = (p-1)(q-1)
    # e*d - 1 = k_mult * phi or e*d + 1 = k_mult * phi
    
    for sign in [1, -1]:
        val = e * d_guess - sign
        
        # For k=1, phi = (p-1)(q-1) ≈ N
        # val should be divisible by phi
        # val / phi = k_mult
        # k_mult ≈ val / N ≈ e * d / N ≈ e (since d ≈ N)
        
        k_mult_approx = val // N
        
        # Now, phi = val / k_mult (approximately)
        # Try k_mult values around k_mult_approx
        for delta in range(-10, 11):
            k_mult = k_mult_approx + delta
            if k_mult <= 0:
                continue
            if val % k_mult != 0:
                continue
            
            phi_guess = val // k_mult
            
            # For k=1: phi = (p-1)(q-1) = N - p - q + 1
            # So p + q = N + 1 - phi
            S = N + 1 - phi_guess
            
            if S <= 0:
                continue
            
            # p, q are roots of x^2 - Sx + N = 0
            disc = S*S - 4*N
            if disc < 0:
                continue
            sqrt_disc = isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                continue
            
            p = (S + sqrt_disc) // 2
            q = (S - sqrt_disc) // 2
            
            if p * q == N and isPrime(p) and isPrime(q):
                print(f"\n[+] FOUND!")
                print(f"    d = {d_guess}")
                print(f"    k_mult = {k_mult}")
                print(f"    sign = {sign}")
                print(f"    phi = {phi_guess}")
                print(f"    p = {p}")
                print(f"    q = {q}")
                
                # Decrypt
                d_real = inverse(e, phi_guess)
                m = pow(enc, d_real, N)
                msg = long_to_bytes(m)
                print(f"    Decrypted: {msg}")
                break
