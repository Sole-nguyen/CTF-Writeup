#!/usr/bin/env python3
"""
Kiss ASIS - Check for special structure in N
Maybe we can factor N directly using factordb or known methods
"""

from Crypto.Util.number import *
from math import gcd, isqrt
import subprocess

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print(f"N = {N}")
print(f"N bits = {N.bit_length()}")

# Check if N is a perfect square
sqrt_N = isqrt(N)
if sqrt_N * sqrt_N == N:
    print(f"N is a perfect square! sqrt(N) = {sqrt_N}")
else:
    print("N is not a perfect square")

# Check small prime factors
print("\nChecking for small prime factors...")
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
for p in small_primes:
    if N % p == 0:
        print(f"N is divisible by {p}!")
        
print("No small prime factors found")

# Check p % 4 == q % 4 == 3 constraint
# This means p ≡ 3 (mod 4) and q ≡ 3 (mod 4)
# So N ≡ p*q ≡ 3*3 = 9 ≡ 1 (mod 4)
print(f"\nN mod 4 = {N % 4}")  # Should be 1

# Check if N could be factored using Fermat's method (for close p, q)
print("\nTrying Fermat factorization...")
a = isqrt(N) + 1
limit = 10**7  # Try up to 10 million iterations

for i in range(limit):
    b_sq = a*a - N
    if b_sq < 0:
        a += 1
        continue
    b = isqrt(b_sq)
    if b * b == b_sq:
        p = a + b
        q = a - b
        if p * q == N:
            print(f"Fermat found factors after {i} iterations!")
            print(f"p = {p}")
            print(f"q = {q}")
            break
    a += 1
    if i % 1000000 == 0:
        print(f"  Iteration {i}...")
else:
    print(f"Fermat failed after {limit} iterations")

# Check GCDs with common values
print("\nChecking GCDs...")
print(f"gcd(N, e) = {gcd(N, e)}")
print(f"gcd(N, e-1) = {gcd(N, e-1)}")
print(f"gcd(N, e+1) = {gcd(N, e+1)}")

# Check if e has special relationship with N
print(f"\ne / N = {e // N} remainder {e % N}")
print(f"e // N bits = {(e // N).bit_length()}")

# For the attack, let's also check:
# If e*d = phi ± 1 for k=3, then e*d = N^3 - (p^3 + q^3) + 1 ± 1
# e*d ≈ N^3

# We can estimate d ≈ N^3 / e
N3 = N ** 3
d_est = N3 // e
print(f"\nEstimated d (N^3/e) = {d_est}")
print(f"Estimated d bits = {d_est.bit_length()}")

# The issue might be that the convergent doesn't hit d exactly
# Let's try a different approach: lattice-based

print("\n" + "="*60)
print("Checking if we can use Coppersmith's method")
print("="*60)

# For Coppersmith, we'd need to find small roots of a polynomial
# In our case, if we knew phi approximately, we could use:
# e*d - 1 ≡ 0 (mod phi)

# But phi = (p^k - 1)(q^k - 1) depends on p, q which we don't know

# Alternative approach: Maybe the vulnerability is simpler
# Let's check if e divides something useful

print(f"\n(N+1) mod e = {(N+1) % e}")
print(f"(N-1) mod e = {(N-1) % e}")

# Check if e is related to N^k - 1
for k in range(1, 7):
    Nk = N ** k
    print(f"\nFor k={k}:")
    print(f"  (N^{k} - 1) mod e = {(Nk - 1) % e}")
    print(f"  (N^{k} + 1) mod e = {(Nk + 1) % e}")
    print(f"  e mod (N^{k}) bits = {(e % Nk).bit_length()}")
