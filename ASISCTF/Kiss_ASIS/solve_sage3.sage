#!/usr/bin/env sage
"""
Kiss ASIS - SageMath LLL/Coppersmith solver

For k=2: phi_2 = (p^2-1)(q^2-1) = (N+1)^2 - (p+q)^2

Let s = p + q. Then:
- phi_2 = (N+1)^2 - s^2
- p*q = N
- p and q are roots of x^2 - s*x + N = 0
- discriminant D = s^2 - 4N must be a perfect square

The key equation: e*d = t*phi_2 + eps where eps in {1, -1}
=> e*d = t*((N+1)^2 - s^2) + eps

Let A = (N+1)^2. Then:
e*d - t*A + t*s^2 = eps

We know:
- d ~ 2^1023 (almost N)
- s ~ 2*sqrt(N) ~ 2^513 
- t ~ e*d/phi ~ e (since d ~ N and phi ~ N^2)

Actually wait, let's recompute:
- e ~ 0.78 * N^2 ~ 0.78 * 2^2046
- d ~ N ~ 2^1023
- phi_2 ~ N^2 ~ 2^2046
- e*d ~ 0.78 * N^3 ~ 0.78 * 2^3069
- t = (e*d - eps) / phi_2 ~ 0.78 * N ~ 0.78 * 2^1023

So t is about 1022 bits, d is about 1023 bits, s is about 513 bits.

For LLL, we need to find small solution to a polynomial.
Let's set up the lattice.

From: e*d - t*A + t*s^2 = eps
=> e*d - t*A + t*s^2 - eps = 0

Variables: d, t, s
Bounds: d ~ 2^1023, t ~ 2^1022, s ~ 2^513

This is multivariate with large unknowns - tricky for standard Coppersmith.

Alternative: Boneh-Durfee for modified phi.
The equation e*d = 1 (mod phi) can be written as:
e*d + k*phi = 1 for some k (note: this k is negative of our t).

For phi = (N+1)^2 - s^2:
e*d + k*((N+1)^2 - s^2) = 1
e*d + k*A - k*s^2 = 1

Modulo e:
k*A - k*s^2 = 1 (mod e)
k*(A - s^2) = 1 (mod e)

So k = inverse(A - s^2, e) = inverse(phi, e)

But we don't know s!

Alternative approach: Use the fact that s^2 - 4N = (p-q)^2.

Let D = s^2 - 4N (discriminant).
Then p = (s + sqrt(D))/2, q = (s - sqrt(D))/2.

We need D to be a perfect square.

Constraint: D = s^2 - 4N >= 0, and D is a perfect square.

From phi = A - s^2:
s^2 = A - phi = (N+1)^2 - phi

And from e*d = t*phi + eps:
phi = (e*d - eps) / t

So s^2 = (N+1)^2 - (e*d - eps)/t = (t*(N+1)^2 - e*d + eps) / t

For s^2 to be a positive integer:
- (t*(N+1)^2 - e*d + eps) must be divisible by t
- Actually (e*d - eps) must be divisible by t first

Let me think differently. Since gcd(e, A) = 49 and 49 divides e:
e = 49 * e' for some e' coprime to A/49

This might give us some structure...

Actually, let me try a practical approach: connect to server multiple times
and hope for weak parameters (small factors, close p and q, etc.)
"""

import sys
from sage.all import *

# Sample data
N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Kiss ASIS - SageMath Solver")
print("="*60)

N = Integer(N)
e = Integer(e)
enc = Integer(enc)

print(f"N bits: {N.nbits()}")
print(f"e bits: {e.nbits()}")

# Check factorization using Sage's builtin
print("\nTrying Sage's factor()...")
try:
    # This might take a while for 1024-bit RSA
    # But let's try with a timeout
    factors = factor(N, limit=10000)
    print(f"Small factors: {factors}")
except Exception as ex:
    print(f"factor() with limit failed: {ex}")

# ECM factorization
print("\nTrying ECM...")
try:
    from sage.libs.pari import pari
    result = pari(N).factorint(flags=2)  # ECM
    print(f"ECM result: {result}")
except Exception as ex:
    print(f"ECM failed: {ex}")

# Try quadratic sieve (for smaller N this would work)
print("\nNote: Full factorization of 1024-bit RSA is computationally infeasible")
print("Need to exploit the special structure of phi = (p^k-1)(q^k-1)")

# Analysis
print("\n" + "="*60)
print("Mathematical Analysis")
print("="*60)

A = (N + 1)^2
print(f"A = (N+1)^2 bits: {A.nbits()}")

g = gcd(e, A)
print(f"gcd(e, (N+1)^2) = {g}")

# For k=2, e/phi should be close to t/d
# And phi ~ A (since s^2 << A)

# Let's compute continued fraction of e/A
print("\nContinued fraction analysis of e/A...")
cf = continued_fraction(e/A)
convergents_list = cf.convergents()

print("Checking first 50 convergents...")
for i, conv in enumerate(convergents_list[:50]):
    t_cand = conv.numerator()
    d_cand = conv.denominator()
    
    if d_cand == 0:
        continue
    
    # Check reasonable bit sizes
    if 1010 <= d_cand.nbits() <= 1030 and t_cand.nbits() >= 1010:
        print(f"\nConvergent {i}: t bits = {t_cand.nbits()}, d bits = {d_cand.nbits()}")
        
        for eps in [1, -1]:
            val = e * d_cand - eps
            if val % t_cand == 0:
                phi_cand = val // t_cand
                print(f"  eps={eps}: phi bits = {phi_cand.nbits()}")
                
                # For k=2: s^2 = A - phi
                s_sq = A - phi_cand
                if s_sq > 0 and is_square(s_sq):
                    s = isqrt(s_sq)
                    disc = s^2 - 4*N
                    if disc >= 0 and is_square(disc):
                        sqrt_disc = isqrt(disc)
                        p = (s + sqrt_disc) // 2
                        q = (s - sqrt_disc) // 2
                        if p * q == N:
                            print(f"  FOUND! p = {p}")
                            print(f"         q = {q}")

print("\n" + "="*60)
print("Trying alternative approach: solve Pell-like equation")
print("="*60)

# The equation s^2 - 4N = D^2 (where D = p - q)
# is a Pell-like equation: s^2 - D^2 = 4N
# (s - D)(s + D) = 4N

# Since 4N = 4*p*q and s - D = 2q, s + D = 2p:
# We need to factor 4N as (2q)(2p)

# But we don't know the factorization!

# Alternative: Coppersmith for small roots
print("\nFor Coppersmith, we would need partial information about p or q.")
print("Without additional structure, 1024-bit RSA is secure.")

print("\n" + "="*60)
print("Conclusion")
print("="*60)
print("This challenge requires either:")
print("1. Server generating weak parameters")
print("2. A sophisticated lattice attack exploiting phi structure")
print("3. External factoring service/software")
