"""
Kiss ASIS - SageMath solver

The attack: 
e = inverse(phi + (-1)^r * d, phi)
=> e * (phi + (-1)^r * d) = 1 (mod phi)
=> e * (-1)^r * d = 1 (mod phi)
=> e * d = (-1)^r (mod phi)

For k_exp = 2:
phi = (p^2 - 1)(q^2 - 1)

Key observation: d is a random prime ~1023 bits
But the relationship e * d = +-1 (mod phi) is special.

Approach: Use Coppersmith's method to find p given partial information.

Actually, let's try a simpler approach first:
Since e * d = t * phi + eps and we know approximate sizes,
we can use LLL to recover t, d.

Run with: sage solve_sage2.sage
"""

import sys
sys.setrecursionlimit(10000)

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("="*60)
print("Kiss ASIS - SageMath Solver")
print("="*60)

print(f"N bits: {N.bit_length()}")
print(f"e bits: {e.bit_length()}")

# Strategy 1: Try small factor base for N
print("\n[1] Checking for small factors of N...")
for p_small in primes(10000):
    if N % p_small == 0:
        print(f"Found small factor: {p_small}")
        q = N // p_small
        break
else:
    print("No small factors found.")

# Strategy 2: Try Fermat factorization
print("\n[2] Trying Fermat factorization...")
a = isqrt(N) + 1
limit = a + 100000
found = False
while a < limit:
    b_sq = a^2 - N
    if is_square(b_sq):
        b = isqrt(b_sq)
        p = a - b
        q = a + b
        if p * q == N:
            print(f"Found factors!")
            print(f"p = {p}")
            print(f"q = {q}")
            found = True
            break
    a += 1

if not found:
    print("Fermat factorization didn't find factors in the tested range.")

# Strategy 3: Use Coppersmith's method
# For k=2: if we know high bits of p, we can use small_roots

print("\n[3] Trying Coppersmith's method...")

# For RSA with modified phi, we can set up a polynomial
# But we need some structure in p or q

# Let's check if N has special structure
print(f"N mod 7 = {N % 7}")
print(f"N + 1 mod 70 = {(N+1) % 70}")  # Since 7 | (N+1)

# Strategy 4: Extended GCD exploration
print("\n[4] GCD analysis...")
g1 = gcd(e, N^2 - 1)
g2 = gcd(e, (N+1)^2)
g3 = gcd(e, (N-1)^2)
print(f"gcd(e, N^2 - 1) = {g1}")
print(f"gcd(e, (N+1)^2) = {g2}")  
print(f"gcd(e, (N-1)^2) = {g3}")

# Try continued fractions on e / N^k for various k
print("\n[5] Continued fractions analysis...")
for k_exp in [1, 2, 3, 4]:
    Nk = N^k_exp
    cf = continued_fraction(e / Nk)
    convergents = cf.convergents()[:200]
    
    print(f"\nk_exp = {k_exp}:")
    for conv in convergents:
        t_cand = conv.numerator()
        d_cand = conv.denominator()
        
        if d_cand == 0 or t_cand == 0:
            continue
        
        # Check if d_cand has right bit length
        if d_cand.bit_length() < 1010 or d_cand.bit_length() > 1030:
            continue
        
        print(f"  Checking t={t_cand.bit_length()} bits, d={d_cand.bit_length()} bits")
        
        # Try to verify
        for eps in [1, -1]:
            val = e * d_cand - eps
            if val % t_cand == 0:
                phi_cand = val // t_cand
                
                # For k_exp = 1: phi = N + 1 - (p+q)
                if k_exp == 1:
                    S = N + 1 - phi_cand
                    if S > 0:
                        disc = S^2 - 4*N
                        if disc >= 0 and is_square(disc):
                            sqrt_disc = isqrt(disc)
                            p = (S + sqrt_disc) // 2
                            q = (S - sqrt_disc) // 2
                            if p * q == N:
                                print(f"  FOUND! k_exp={k_exp}, eps={eps}")
                                print(f"  p = {p}")
                                print(f"  q = {q}")
                                
                                # Decrypt
                                phi = (p - 1) * (q - 1)
                                d = inverse_mod(e, phi)
                                m = power_mod(enc, d, N)
                                from Crypto.Util.number import long_to_bytes
                                print(f"  msg = {long_to_bytes(int(m))}")
                                sys.exit(0)
                
                # For k_exp = 2: phi = (N+1)^2 - S^2
                elif k_exp == 2:
                    S_sq = (N+1)^2 - phi_cand
                    if S_sq > 0 and is_square(S_sq):
                        S = isqrt(S_sq)
                        disc = S^2 - 4*N
                        if disc >= 0 and is_square(disc):
                            sqrt_disc = isqrt(disc)
                            p = (S + sqrt_disc) // 2
                            q = (S - sqrt_disc) // 2
                            if p * q == N:
                                print(f"  FOUND! k_exp={k_exp}, eps={eps}")
                                print(f"  p = {p}")
                                print(f"  q = {q}")
                                
                                # Decrypt
                                phi = (p^2 - 1) * (q^2 - 1)
                                d = inverse_mod(e, phi)
                                m = power_mod(enc, d, N)
                                from Crypto.Util.number import long_to_bytes
                                print(f"  msg = {long_to_bytes(int(m))}")
                                sys.exit(0)

print("\n[6] Trying Pollard p-1...")
# Pollard p-1 with bound B
def pollard_pm1(n, B=100000):
    a = 2
    for p in primes(B):
        e_p = int(log(B, p))
        a = power_mod(a, p^e_p, n)
        if a == 0:
            return None
        g = gcd(a - 1, n)
        if 1 < g < n:
            return g
    return None

factor = pollard_pm1(N, 100000)
if factor:
    print(f"Pollard p-1 found factor: {factor}")
else:
    print("Pollard p-1 didn't find a factor with B=100000")

print("\n[7] Trying Williams p+1...")
# Williams p+1 factorization
def williams_pp1(n, B=100000):
    # Use Lucas sequences
    from sage.all import lucas_number1
    
    for A in range(3, 50):
        v = A
        for p in primes(B):
            e_p = int(log(B, p))
            for _ in range(e_p):
                # v = lucas_number1(p, A, 1) mod n
                # This is slow, use fast modular Lucas
                v = (v^p) % n  # Simplified, not correct but faster
        g = gcd(v - 2, n)
        if 1 < g < n:
            return g
    return None

# Skip Williams for now as it needs proper implementation

print("\n[8] ECM factorization...")
try:
    p = ecm.factor(N, B1=10000, B2=100000)
    print(f"ECM found factors: {p}")
except:
    print("ECM didn't find factors quickly")

print("\n[9] Full factorization (may take a while)...")
try:
    factors = factor(N)
    print(f"Factors: {factors}")
    
    if len(factors) == 2:
        p = int(factors[0][0])
        q = int(factors[1][0])
        
        print(f"p = {p}")
        print(f"q = {q}")
        
        # Try all k values to decrypt
        for k in range(1, 7):
            try:
                phi = (p^k - 1) * (q^k - 1)
                d = inverse_mod(e, phi)
                m = power_mod(enc, d, N)
                from Crypto.Util.number import long_to_bytes
                msg = long_to_bytes(int(m))
                if all(32 <= c <= 126 for c in msg):
                    print(f"k={k}: {msg}")
            except Exception as ex:
                print(f"k={k}: Failed - {ex}")
except Exception as ex:
    print(f"Factorization failed: {ex}")

print("\n" + "="*60)
print("Done.")
print("="*60)
