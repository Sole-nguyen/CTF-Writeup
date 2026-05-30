#!/usr/bin/env python3
"""
Kiss ASIS - Exploit d being prime

We have: e*d = t*phi +/- 1
So: e*d ≡ +/-1 (mod phi)
And: e*d ≡ +/-1 (mod any_factor_of_phi)

For k=2: phi = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)

Since p ≡ q ≡ 3 (mod 4) (Blum primes):
- p-1 ≡ 2 (mod 4)
- p+1 ≡ 0 (mod 4)
- Similarly for q

So phi is divisible by 2^4 = 16 at minimum.

Actually, let's think about this differently.

For fixed sample data, let's compute what constraints we have.

e*d - t*phi = +/-1

If we knew the order of e modulo some number related to N...
ord_e (mod p^k - 1) would be related to d

Actually wait - in the encryption, m^e mod N is computed.
If we could compute m^(e*d) mod N, we'd get m^(±1 mod phi) = m or m^(-1)

But we only have enc = m^e mod N, not m.

Hmm, let me try another angle.

For k, we have: e*d = t*phi_k + r
So: t = (e*d - r) / phi_k

For this to be a positive integer:
1. phi_k must divide (e*d - r)
2. t > 0

Now, e and phi_k share no common factors (since e has an inverse mod phi_k).
So gcd(e, phi_k) = 1.

This gives us constraints on phi_k and hence on p, q.

Let's check the sample data to verify k=2:
"""

from Crypto.Util.number import *
from math import isqrt, gcd

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")
print(f"Ratio e_bits/n_bits: {e.bit_length() / N.bit_length():.2f}")

# Check for small factor of e
print("\nSmall factors of e:")
e_temp = e
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    cnt = 0
    while e_temp % p == 0:
        cnt += 1
        e_temp //= p
    if cnt > 0:
        print(f"  {p}^{cnt}")

# e / N^k for various k
print("\ne / N^k ratios:")
for k in range(1, 7):
    ratio = e / (N**k)
    print(f"  k={k}: {ratio:.10e}")

# For k=2, ratio ~ 0.78 means t/d ~ 0.78
# t ~ 0.78 * d

# Since d ~ N^0.999 ~ 2^1023 and t ~ 0.78*d ~ 2^1021
# This is huge!

# Let's think about modular arithmetic
# e*d = t*phi + r
# e = inverse(phi + (-1)^r * d, phi)

# Note: inverse(a, m) = pow(a, -1, m) = a^(phi(m)-1) mod m when gcd(a,m)=1
# But inverse(phi + sign*d, phi) = inverse(sign*d, phi) since phi ≡ 0 (mod phi)
# So e = inverse(sign*d, phi) = (sign*d)^(-1) mod phi
# e * (sign * d) ≡ 1 (mod phi)
# e * d ≡ sign (mod phi) where sign = +1 or -1

# So e*d mod phi = 1 or phi-1

# Now, what is e mod (small primes)?
print("\ne mod small primes:")
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    print(f"  e mod {p} = {e % p}")

# Check if e has special form
print(f"\ne mod (N+1) = {e % (N+1)}")
print(f"e mod (N-1) = {e % (N-1)}")

# Try to find relationship
# e / (N+1)^2:
A = (N+1)**2
print(f"\ne / (N+1)^2 = {e / A:.10f}")

# If e*d = t*phi + 1 and phi = A - s^2:
# e*d = t*(A - s^2) + 1 = t*A - t*s^2 + 1

# e*d mod A = -t*s^2 + 1 mod A

# Hmm, we still have unknowns d, t, s...

# Let's try continued fractions on e/A
print("\nContinued fraction analysis of e / (N+1)^2:")

def cf(n, d, limit=20):
    """Get continued fraction coefficients"""
    coeffs = []
    while d != 0 and len(coeffs) < limit:
        q = n // d
        coeffs.append(q)
        n, d = d, n - q*d
    return coeffs

def convergent(cf_coeffs, i):
    """Get i-th convergent from cf coefficients"""
    if i < 0 or i >= len(cf_coeffs):
        return None, None
    h0, h1 = 0, 1
    k0, k1 = 1, 0
    for j in range(i+1):
        a = cf_coeffs[j]
        h2 = a * h1 + h0
        k2 = a * k1 + k0
        h0, h1 = h1, h2
        k0, k1 = k1, k2
    return h1, k1

cf_coeffs = cf(e, A, 50)
print(f"First 20 CF coefficients: {cf_coeffs[:20]}")

for i in range(min(20, len(cf_coeffs))):
    t, d = convergent(cf_coeffs, i)
    if d and d > 0:
        print(f"Convergent {i}: t/d = {t}/{d} = {t/d:.6f}, d bits = {d.bit_length()}")

# These convergents give us approximations to e/A
# For the correct t/d, we should have e*d - t*A ≈ t*s^2 - 1

# Since s ~ 2*sqrt(N) ~ 2^513, s^2 ~ 2^1026 ~ N^2 ~ A
# So t*s^2 ~ t*A, which means e*d - t*A ~ t*A - 1 => e*d ~ 2*t*A

# This suggests e/A ~ 2t/d, not t/d
# So let's try e/(2*A):
print("\nContinued fraction analysis of e / (2*(N+1)^2):")
cf_coeffs2 = cf(e, 2*A, 50)
print(f"First 10 CF coefficients: {cf_coeffs2[:10]}")

# Actually the issue is s^2/A is small, around 4N/N^2 = 4/N ~ 0
# So phi ~ A - tiny ≈ A

# Therefore e/phi ~ e/A ~ t/d

# The issue is that t and d are both huge (~N), so the continued 
# fraction doesn't converge quickly enough.

print("\n" + "="*60)
print("Trying alternative: Lucas sequences")
print("="*60)

# For encryption c = m^e mod N
# Decryption: m = c^d mod N where e*d ≡ 1 (mod phi)
# 
# But we have e*d ≡ ±1 (mod phi)
# If e*d ≡ 1 (mod phi): c^d = m
# If e*d ≡ -1 (mod phi): c^d = m^(-1) mod N

# Can we compute c^d without knowing d?
# We need to find d such that e*d ≡ 1 or -1 (mod phi)

# If we can factor N, we can compute phi and then d = e^(-1) mod phi

# Let's try some factorization methods again

print("\nFermat factorization with larger range:")
a = isqrt(N) + 1
for i in range(1000000):
    b2 = a*a - N
    b = isqrt(b2)
    if b*b == b2:
        p = a - b
        q = a + b
        print(f"Found at iteration {i}!")
        print(f"p = {p}")
        print(f"q = {q}")
        break
    a += 1
    if i % 100000 == 0:
        print(f"  Fermat: {i} iterations...")
else:
    print("  Fermat failed within limit")

# Try Pollard's p-1
print("\nPollard p-1 method:")
a = 2
for B in [10000, 50000, 100000]:
    aa = a
    for j in range(2, B+1):
        aa = pow(aa, j, N)
    g = gcd(aa - 1, N)
    if 1 < g < N:
        print(f"Found with B={B}! p = {g}")
        break
else:
    print("  Pollard p-1 failed")

print("\nDone with sample analysis.")
