#!/usr/bin/env python3
"""
Kiss ASIS - Exploit gcd(e, (N+1)^2) = 49
"""

from Crypto.Util.number import *
from math import isqrt, gcd

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Exploiting gcd(e, (N+1)^2) = 49")
print("="*60)

# gcd(e, (N+1)^2) = 49
# This means 7^2 | e and 7 | (N+1)
# So 7 | (N+1), meaning N = -1 (mod 7), i.e., N = 6 (mod 7)

print(f"N mod 7 = {N % 7}")
print(f"(N+1) mod 7 = {(N+1) % 7}")
print(f"e mod 7 = {e % 7}")
print(f"e mod 49 = {e % 49}")

# So 7 | (N+1) = p*q + 1
# This means p*q = -1 (mod 7)

# For k=2: phi_2 = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)
# Let's check: gcd(e, phi_2_estimate)

# phi_2 = (N+1)^2 - S^2 where S = p + q
# Since 7 | (N+1), we have 49 | (N+1)^2
# So phi_2 mod 49 = -S^2 mod 49

# Hmm, let me think about this differently...

# We know: e * d = t * phi_k + eps  (eps = 1 or -1)
# And e is divisible by 49

# Since gcd(e, phi) needs to equal 1 for d to exist...
# Actually no, we have e = inverse(phi + sign*d, phi)
# So e * (phi + sign*d) = 1 (mod phi)
# => e * sign * d = 1 (mod phi)
# => gcd(e*d, phi) = 1

# This means 7 cannot divide phi!
# But for k=2: phi_2 = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)

# If 7 | phi_2, then 7 | (p-1), 7 | (p+1), 7 | (q-1), or 7 | (q+1)
# i.e., p = 1, -1, 1, or -1 (mod 7)
# i.e., p = 1, 6, 1, or 6 (mod 7)

# For e*d to be coprime to phi, we need 7 not divide phi
# So p != 1, 6 (mod 7) and q != 1, 6 (mod 7)
# i.e., p, q in {2, 3, 4, 5} (mod 7)

# But we also have p*q = -1 (mod 7) = 6 (mod 7)
# Pairs (p mod 7, q mod 7) with p*q = 6 (mod 7):
# 2*3 = 6 ✓
# 3*2 = 6 ✓
# 4*5 = 20 = 6 ✓
# 5*4 = 20 = 6 ✓
# All these avoid 1 and 6! So this is consistent.

print("\nThis is consistent with k=2 (7 does not divide phi_2)")

# Now, let's use another insight
# e/49 should also have some structure

e_div_49 = e // 49
print(f"\ne // 49 has {e_div_49.bit_length()} bits")
print(f"gcd(e//49, N+1) = {gcd(e_div_49, N+1)}")

# Let's check if (N+1) // 7 divides e
N_plus_1_div_7 = (N+1) // 7
print(f"\n(N+1) // 7 has {N_plus_1_div_7.bit_length()} bits")
print(f"gcd(e, (N+1)//7) = {gcd(e, N_plus_1_div_7)}")
print(f"gcd(e//49, (N+1)//7) = {gcd(e_div_49, N_plus_1_div_7)}")

# Let's factor N+1 a bit more
print("\nFactoring N+1 by small primes:")
temp = N + 1
small_factors = []
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    while temp % p == 0:
        small_factors.append(p)
        temp //= p
print(f"N+1 = {small_factors} * ...")
print(f"Remaining cofactor has {temp.bit_length()} bits")

# Check if cofactor relates to e
print(f"gcd(e, remaining cofactor) = {gcd(e, temp)}")

# Let's think about this more carefully
# For k=2, phi_2 = (N+1)^2 - S^2 = (N+1-S)(N+1+S)
# We have 49 | e and 7 | (N+1)
# So 7 | (N+1+S) or 7 | (N+1-S) depends on S mod 7

print("\n" + "="*60)
print("Alternative: try Fermat factorization variants")
print("="*60)

# If p and q are close, Fermat works
# Let's try various distances

def fermat_factor(n, max_iter=10000000):
    a = isqrt(n) + 1
    b2 = a*a - n
    
    for i in range(max_iter):
        b = isqrt(b2)
        if b*b == b2:
            return a - b, a + b
        a += 1
        b2 = a*a - n
        
        if i % 1000000 == 0 and i > 0:
            print(f"  Fermat: tried {i} iterations...")
    
    return None, None

print("Running Fermat factorization...")
p, q = fermat_factor(N, 1000000)
if p:
    print(f"Found: p = {p}, q = {q}")
else:
    print("Fermat didn't find close factors within limit")

# Try Pollard's rho
print("\nTrying Pollard's rho...")

def pollard_rho(n, max_iter=1000000):
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    # f(x) = x^2 + 1 mod n
    f = lambda x: (x * x + 1) % n
    
    iterations = 0
    while d == 1 and iterations < max_iter:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        iterations += 1
        
        if iterations % 100000 == 0:
            print(f"  Pollard: {iterations} iterations...")
    
    if d != n and d != 1:
        return d
    return None

factor = pollard_rho(N, 500000)
if factor:
    print(f"Found factor: {factor}")
    q = N // factor
    print(f"p = {factor}, q = {q}")
else:
    print("Pollard's rho didn't find a factor")

# ECM would be better but needs more setup
print("\n" + "="*60)
print("Let's check if maybe k=1 and we missed something")  
print("="*60)

# For k=1: phi_1 = (p-1)(q-1) = N - (p+q) + 1
# e*d = t*phi_1 + eps
# Given e ~ N^2 and d ~ N, e*d ~ N^3
# phi_1 ~ N
# So t ~ N^2 - way too big

# But wait - check gcd for k=1
# phi_1 = (p-1)(q-1)
# For gcd(e, phi_1) = 1, we need 7 not divide (p-1)(q-1)
# i.e., p != 1 (mod 7) and q != 1 (mod 7)
# With p*q = 6 (mod 7), this is possible

# Hmm, what if the challenge uses k=1 but with a different relationship?

# Actually, let me re-read the source code insight:
# e = inverse(phi + (-1)^r * d, phi)
# means e * (phi + (-1)^r * d) = 1 (mod phi)
# => e * (-1)^r * d = 1 (mod phi)

# If r = 0: e * d = 1 (mod phi)
# If r = 1: e * d = -1 (mod phi), i.e., e * d = phi - 1 (mod phi)

# So e * d mod phi is either 1 or phi-1

# For k=2, phi ~ N^2
# e ~ 0.776 * N^2
# d ~ N

# e * d ~ 0.776 * N^3
# This should equal t * phi + eps for some t
# 0.776 * N^3 = t * N^2 * (1 - small) + eps
# t ~ 0.776 * N

# So t is around 0.776 * N, which is a ~1022 bit number

print(f"\nFor k=2, estimated t is around 0.776 * N")
print(f"0.776 * N has {int(0.776 * N).bit_length()} bits")

# This is still a huge search space...

# Let me try a lattice approach using LLL
print("\n" + "="*60)
print("Setting up LLL for k=2")
print("="*60)

# For k=2: e*d - t*phi = eps (eps = +/- 1)
# phi = (N+1)^2 - S^2
# We want to find t, d, S such that:
# e*d - t*((N+1)^2 - S^2) = eps

# This is a polynomial equation in multiple unknowns - tricky for LLL

# Alternative: use the approximation
# e/((N+1)^2) ~ t/d * (1 + S^2/((N+1)^2 - S^2))
# Since S^2 << (N+1)^2, this is approximately t/d

# Actually for k=2, the issue is S^2/N^2 ~ 4N/N^2 = 4/N which is tiny
# So e/N^2 ~ t/d very closely

# We have e/N^2 = 0.7758711844...
# We need to find fraction t/d where d ~ N

# This is just approximating 0.7758711844 as a fraction!
# Let's compute the continued fraction of e/N^2

from fractions import Fraction

ratio = Fraction(e, N*N)
print(f"e / N^2 as fraction = {ratio}")
print(f"numerator bits: {ratio.numerator.bit_length()}")
print(f"denominator bits: {ratio.denominator.bit_length()}")

# The numerator and denominator should give us t and d!
# But wait, they might have common factors with the "small correction"

# Let's verify: if t = ratio.numerator and d = ratio.denominator
# Then e/N^2 = t/d exactly
# So e*d = t*N^2
# We need e*d = t*phi + eps
# So t*N^2 = t*phi + eps
# t*(N^2 - phi) = eps
# For k=2: N^2 - phi = N^2 - (N+1)^2 + S^2 = N^2 - N^2 - 2N - 1 + S^2 = S^2 - 2N - 1
# t * (S^2 - 2N - 1) = eps = +/- 1

# Hmm, this means t * (S^2 - 2N - 1) = +/- 1
# For this to have an integer solution, we need S^2 - 2N - 1 = +/- 1/t or +/- t

# If t ~ 0.776 * N, then S^2 - 2N - 1 ~ 1/t ~ 0 is impossible
# Unless... t is actually small and we're wrong about the sizes

# Wait, let me reconsider. Let's compute what t and d would be:
t_exact = ratio.numerator
d_exact = ratio.denominator
print(f"\nt (from e/N^2) = {t_exact}")
print(f"d (from e/N^2) = {d_exact}")
print(f"t bits: {t_exact.bit_length()}")
print(f"d bits: {d_exact.bit_length()}")

# Check gcd
g = gcd(e, N*N)
print(f"\ngcd(e, N^2) = {g}")

# If e and N^2 are coprime, the fraction is already in lowest terms
# and d_exact = N^2, which is wrong (d should be ~ N)

# So this approach doesn't directly give us t, d
