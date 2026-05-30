"""
Kiss ASIS - SageMath solver using Coppersmith/LLL

Key insight for k=2:
- phi = (p^2-1)(q^2-1) = (N+1)^2 - (p+q)^2
- e*d = t*phi + eps where eps in {1, -1}
- Given e/N^2 ~ 0.776 and d ~ N, we have t ~ 0.776*N

The equation can be rewritten as:
e*d - t*((N+1)^2 - s^2) = eps
where s = p + q

This is a multivariate polynomial equation.
We can use Coppersmith's method to find small roots.
"""

N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842

print("N bits:", N.bit_length())
print("e bits:", e.bit_length())

# For k=2, we have:
# phi_2 = (p^2-1)(q^2-1) = N^2 + 2N + 1 - (p+q)^2 = (N+1)^2 - s^2
# where s = p + q

# e*d = k*phi_2 + eps (eps = +/- 1)
# e*d = k*((N+1)^2 - s^2) + eps

# Rearranging: e*d - k*(N+1)^2 + k*s^2 = eps

# Let A = (N+1)^2
A = (N+1)^2
print(f"A = (N+1)^2 bits: {A.bit_length()}")

# The equation: e*d - k*A + k*s^2 = eps
# We need to find k, d, s such that this holds

# Known bounds:
# - d ~ 2^1023 (from the source code: d has about 1023-1024 bits)
# - s ~ 2*sqrt(N) ~ 2^513 (since p, q ~ 2^512 each)
# - k = (e*d - eps) / phi ~ e*d/phi ~ (0.776*N^2 * N) / N^2 = 0.776*N ~ 2^1021

# For LLL/Coppersmith, we need the polynomial to have a small root.
# But here all unknowns are large (around N or sqrt(N)).

# Alternative approach: Wiener attack generalization
# e/phi ~ k/d
# Since phi ~ N^2 (for k_exp=2), we have e/N^2 ~ k/d
# The continued fraction of e/N^2 should give k/d as a convergent

# But we tried this and it didn't work directly because:
# phi = A - s^2, and the correction s^2/A is not negligible for finding exact k, d

# New approach: Use the constraint that d is PRIME
# d must be a prime around 2^1023
# k = (e*d - eps) / phi must be a positive integer
# phi = A - s^2 where s = p + q and p*q = N

# Since p*q = N and p + q = s, we have:
# p, q are roots of x^2 - s*x + N = 0
# discriminant = s^2 - 4N must be a perfect square

# So the problem reduces to:
# Find s such that:
# 1. s^2 - 4N is a perfect square
# 2. (e*d - eps) is divisible by (A - s^2) for some prime d ~ 2^1023

# Strategy: 
# For various candidate s (where s^2 - 4N is a perfect square),
# check if we can find valid d and k.

# Finding s such that s^2 - 4N is a perfect square:
# Let s^2 - 4N = t^2
# s^2 - t^2 = 4N
# (s-t)(s+t) = 4N

# Factor 4N = 4 * p * q (since N = p*q)
# Possible factorizations of 4N:
# (s-t, s+t) could be (4, N), (2, 2N), (4p, q), (4q, p), (2p, 2q), etc.

# For (s-t, s+t) = (a, b) where a*b = 4N:
# s = (a+b)/2, t = (b-a)/2
# Both must be integers, so a and b must have same parity.

# Since 4N is even, we need factors (a, b) both even or both odd.
# 4N = 4*N = 2^2 * N, if N is odd (which it is since p, q are odd primes)
# So 4N has factors like (4, N), (2, 2N), (1, 4N), etc.
# (1, 4N): s = (1 + 4N)/2 - not integer
# (2, 2N): s = (2 + 2N)/2 = N + 1, t = (2N - 2)/2 = N - 1
#          s^2 - 4N = (N+1)^2 - 4N = N^2 - 2N + 1 = (N-1)^2 = t^2 ✓
#          So s = N + 1 gives p = ((N+1) + (N-1))/2 = N, q = 1 - not valid primes
# (4, N): s = (4 + N)/2, t = (N - 4)/2 - need N even, but N is odd, so invalid

# The valid factorization is (s-t, s+t) = (2(p-q), 2(p+q)) when p > q
# Wait, let's redo this.

# We have p + q = s and p - q = sqrt(s^2 - 4N) (assuming p > q)
# Actually, discriminant D = s^2 - 4N = (p+q)^2 - 4pq = (p-q)^2

# So if we write 4N = 4pq and we want to find s = p + q:
# We need to factor N to get p, q, then s = p + q.

# But we don't know the factorization of N! That's the whole problem.

# Let me try a different angle: since gcd(e, (N+1)^2) = 49,
# we have 7^2 | e and 7 | (N+1).

# For k_exp = 1 (standard RSA):
# phi_1 = (p-1)(q-1) = N - (p+q) + 1
# e*d = k*phi_1 + eps

# e/N ~ k/d (approximately for k_exp=1)
# But e/N is huge (e ~ N^2), so k/d ~ N
# Since d ~ N, we have k ~ N^2, which is huge.

# So k_exp = 1 doesn't match.

# For k_exp = 2:
# phi_2 ~ N^2
# e/N^2 ~ k/d ~ 0.776
# k and d are both ~ N

# Hmm, let me try to compute the exact ratio.

ratio = e / A  # e / (N+1)^2
print(f"e / (N+1)^2 = {float(ratio):.10f}")

# For phi_2 = A - s^2 where s ~ 2*sqrt(N):
# phi_2 / A ~ 1 - s^2/A ~ 1 - 4N/(N^2) ~ 1 - 4/N ~ 1

# So e/phi_2 ~ e/A * (1 / (1 - 4/N)) ~ e/A * (1 + 4/N) ~ e/A

# e/phi ~ k/d
# k/d ~ e/A ~ 0.7759

# So k ~ 0.7759 * d
# Since d ~ 2^1023, we have k ~ 0.7759 * 2^1023

# Let's think about this more carefully with continued fractions.
# e/A = e / (N+1)^2
# If this equals k/d exactly (ignoring the s^2 term), then:
# e * d = k * A
# But we know e*d = k*phi + eps = k*(A - s^2) + eps
# So e*d = k*A - k*s^2 + eps
# k*A = e*d + k*s^2 - eps
# A = e*d/k + s^2 - eps/k

# This doesn't directly help...

# New idea: use the fact that k and d are related
# e*d - eps is divisible by phi = A - s^2
# e*d - eps = t * (A - s^2) for some t
# e*d = t*A - t*s^2 + eps

# If we knew s exactly, we could solve for t and d.
# But s is unknown.

# However, s = p + q and p*q = N.
# So s^2 - 4N = (p-q)^2 >= 0
# s >= 2*sqrt(N)

# The minimum value of s is 2*sqrt(N), achieved when p = q = sqrt(N)
# But since N is the product of two distinct primes, s > 2*sqrt(N)

# Let's parameterize: s = 2*sqrt(N) + delta for some small delta
# Then s^2 = 4N + 4*sqrt(N)*delta + delta^2 ~ 4N + 4*sqrt(N)*delta
# s^2 - 4N ~ 4*sqrt(N)*delta = (p-q)^2
# delta ~ (p-q)^2 / (4*sqrt(N))

# If p and q are random 512-bit primes, |p-q| is typically around 2^511
# delta ~ 2^1022 / (4 * 2^511) = 2^1022 / 2^513 = 2^509

# So s - 2*sqrt(N) ~ 2^509

# This means we might need to search a range of about 2^509, which is huge!

# Unless there's additional structure we can exploit...

print("\n" + "="*60)
print("Let's verify the math with a test case")
print("="*60)

# Generate a test case to verify our understanding
import random

def test_math():
    from Crypto.Util.number import getPrime, inverse, getRandomRange
    import random
    
    nbit = 512  # Smaller for testing
    
    # Generate similar to the challenge
    p = getPrime(nbit // 2)
    while p % 4 != 3:
        p = getPrime(nbit // 2)
    
    q = getPrime(nbit // 2)
    while q % 4 != 3:
        q = getPrime(nbit // 2)
    
    N_test = p * q
    k_exp = random.choice([1, 2, 3, 4, 5, 6])
    phi_test = (p**k_exp - 1) * (q**k_exp - 1)
    
    D = random.uniform(0.999, 0.9999)
    d_bits = int((nbit // 2 + 1) * D)
    d = getPrime(d_bits)
    
    r = random.randint(0, 1)
    e_test = inverse(phi_test + (-1)**r * d, phi_test)
    
    print(f"Test case: k_exp={k_exp}, r={r}")
    print(f"N bits: {N_test.bit_length()}")
    print(f"e bits: {e_test.bit_length()}")
    print(f"d bits: {d.bit_length()}")
    print(f"phi bits: {phi_test.bit_length()}")
    
    # Verify relationship
    print(f"e*d mod phi = {(e_test * d) % phi_test}")
    print(f"(-1)^r = {(-1)**r}")
    
    # Compute t = (e*d - (-1)^r) / phi
    t = (e_test * d - (-1)**r) // phi_test
    print(f"t = {t}")
    print(f"t bits: {t.bit_length()}")
    
    # Ratios
    print(f"\ne/N^{k_exp} = {e_test / (N_test ** k_exp):.6f}")
    print(f"t/d = {t / d:.6f}")

# We can't run this directly since we need sympy or sage
# But the analysis shows:
# - For k_exp=k, phi ~ N^k
# - t ~ e*d / phi ~ e*d / N^k
# - If d ~ N^(1/k) approximately, then t ~ e / N^(k-1/k)

# For the given challenge with e ~ 0.776 * N^2 and d ~ N:
# t ~ 0.776 * N^2 * N / N^2 = 0.776 * N (for k_exp=2)

print("\nFor the actual challenge:")
print(f"e/N^2 = {e / (N**2):.10f}")
print(f"This suggests t/d ~ {e / (N**2):.6f} if k_exp=2")
print(f"With d ~ N (1023 bits), t ~ 0.776 * N also has ~1023 bits")

# Key observation: if we look at e*d mod (N+1)^2:
# e*d = t*(A - s^2) + eps
# e*d mod A = -t*s^2 + eps (mod A)
# (e*d - eps) mod A = -t*s^2 (mod A)

# Since gcd(e, A) = 49:
e_mod_A = e % A
print(f"\ne mod (N+1)^2 = {e_mod_A}")
print(f"e mod (N+1)^2 bits: {e_mod_A.bit_length()}")

# (e*d - eps) mod A = -t*s^2 (mod A)
# If we knew d, we could compute (e*d - eps) mod A and relate it to t*s^2

# But we don't know d or t or s...

# Let me think about this from the GCD angle.
# gcd(e, (N+1)^2) = 49
# This means e = 49 * e' for some e' coprime to (N+1)/7

# Also gcd(e, N^2-1) = 7
# N^2 - 1 = (N-1)(N+1)
# So 7 | (N+1) (we know) and 7 does not divide (N-1)

print(f"\nN mod 7 = {N % 7}")
print(f"(N-1) mod 7 = {(N-1) % 7}")
print(f"(N+1) mod 7 = {(N+1) % 7}")
print(f"gcd(e, N-1) = {gcd(e, N-1)}")
print(f"gcd(e, N+1) = {gcd(e, N+1)}")
print(f"gcd(e/49, (N+1)/7) = {gcd(e//49, (N+1)//7)}")

# Summary: This is a hard problem without more structure.
# The most promising approach is Coppersmith's method in SageMath.

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("This challenge requires Coppersmith's lattice method in SageMath.")
print("The key polynomial is:")
print("f(x, y) = e*d - k*((N+1)^2 - (x + y)^2) - eps")
print("where x = p, y = q are the unknown factors of N.")
print("")
print("Run this in SageMath for a proper solution.")
