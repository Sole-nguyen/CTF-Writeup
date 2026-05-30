#!/usr/bin/env python3
"""
Kiss ASIS - Try sympy LLL or flatter

Since d is a PRIME approximately 1023-1024 bits, and e*d = t*phi + eps,
we have the equation:

e*d - t*phi = eps (where eps = +/-1)

For k=2: phi = (p^2-1)(q^2-1) = (N+1)^2 - S^2 where S = p+q

Substituting:
e*d - t*((N+1)^2 - S^2) = eps
e*d - t*(N+1)^2 + t*S^2 = eps

Let A = (N+1)^2. Then:
e*d - t*A + t*S^2 = eps

Rearranging:
e*d = t*(A - S^2) + eps

Since we don't know d, t, or S, we need to find them.

Key observation: S ~ 2*sqrt(N), so S^2 ~ 4N, and A - S^2 ~ N^2 - 4N ~ N^2

The continued fraction of e/A gives approximations to t/d.

But the issue is t and d are both ~N, so the approximation needs
to be EXACT (or very close) for this to work.

Alternative approach:
Use the fact that d is PRIME and search for primes d near the 
continued fraction approximations.
"""

from sympy import isprime, Integer, Rational, continued_fraction, continued_fraction_convergents, continued_fraction_iterator
from Crypto.Util.number import *
from math import isqrt, gcd
import sys

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("Testing sympy...")

# Check basic sympy works
try:
    from sympy import Matrix, sqrt, Abs
    print("sympy imported successfully")
except ImportError as ie:
    print(f"sympy import error: {ie}")
    sys.exit(1)

A = (N+1)**2
print(f"A bits: {A.bit_length()}")

# Create rational approximation
ratio = Rational(e, A)
print(f"e/A ratio created")

# Get continued fraction
cf = continued_fraction(ratio)
print(f"Continued fraction created")

# Get convergents
count = 0
for conv in continued_fraction_convergents(cf):
    t, d = conv.p, conv.q
    if d <= 1:
        continue
    
    # Check if this d is close to what we expect (~1023 bits)
    if d.bit_length() >= 100:  # Start checking from reasonable size
        # For each convergent (t, d), check if e*d - t*A is close to a valid value
        
        val = e * d - t * A
        
        # For k=2: e*d = t*phi + eps = t*(A - S^2) + eps
        # So e*d - t*A = -t*S^2 + eps
        # => val = -t*S^2 + eps
        # => t*S^2 = -val + eps
        
        for eps in [1, -1]:
            s_sq_t = eps - val
            if s_sq_t > 0 and s_sq_t % t == 0:
                s_sq = s_sq_t // t
                if s_sq > 0:
                    s = isqrt(s_sq)
                    if s * s == s_sq:
                        print(f"\nPotential solution found!")
                        print(f"d = {d}")
                        print(f"t = {t}")
                        print(f"s = {s}")
                        
                        # Verify: p, q from s
                        disc = s*s - 4*N
                        if disc >= 0:
                            sqrt_disc = isqrt(disc)
                            if sqrt_disc * sqrt_disc == disc:
                                p = (s + sqrt_disc) // 2
                                q = (s - sqrt_disc) // 2
                                if p * q == N:
                                    print(f"FOUND FACTORS!")
                                    print(f"p = {p}")
                                    print(f"q = {q}")
    
    count += 1
    if count % 100 == 0:
        print(f"Checked {count} convergents, d bits: {d.bit_length() if d > 0 else 0}")
    
    if count > 5000:
        print("Reached limit")
        break

print("Done")
