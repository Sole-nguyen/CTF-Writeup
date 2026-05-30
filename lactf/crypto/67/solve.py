#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, isPrime
import itertools

# Challenge values
n = 3065166648989946543243321749182110380130600495836529115324962314953602410955238274815048102133926473802784509364164598272123253170429833062111406183967892776205128428451881191306636266223693247774152023376966072838972795687447000874551965634001135157574180761259512684571042760684073773235677990991922855678255765281887363759691793233620651487345583516498648719919707128917609302334790978072680179152873
c = 2418087796246063177805307534754575241040737138492067274273250868514896709117922810300359507039955869689143476512994256581930747034099418821478357134257494981186446615338255149311007890473021946231218239782857504280299517112774518325466639635307819626466714694914642918330145279619365599285904572343699693898032821941138788768596346568499295165234261818748205275543063022185741912452700186380381125193892
e = 65537

# The prime p has structure: 666...666 (67 sixes) + middle (67 random 6s or 7s) + 777...777 (67 sevens)
# Total: 201 digits

# Build the known parts
prefix = "6" * 67  # 67 sixes
suffix = "7" * 67  # 67 sevens
middle_len = 67

print("Brute forcing the middle 67 digits...")
print(f"Total possibilities: 2^67 = {2**67}")
print("This is too large to brute force directly.")
print()

# Since we can't brute force 2^67, we need a smarter approach
# Let's use the fact that p divides n
# We can try to recover p using Coppersmith's attack or similar

# Alternative: Check if there's a pattern or use integer factorization
# Since p is about 201 digits and n is about 402 digits, q should be about 670 bits (201 digits)
# Actually, q is getPrime(670) which is 670 bits, not digits!

# Let's calculate: p is 201 decimal digits ≈ 668 bits
# q is 670 bits
# n should be about 1338 bits

n_bits = n.bit_length()
print(f"n has {n_bits} bits")

# Since we know most of p, we can try a Coppersmith-like approach
# Or since the unknown part is in the middle, we can try partial key recovery

# Let's try a meet-in-the-middle approach
# Split the 67 unknown digits into two halves

# Actually, with 67 unknown binary choices, this is still too large
# Let's check if maybe the server reuses primes or has a weakness

# Better approach: Use Fermat factorization since p and q are close in size
def fermat_factor(n, max_iter=100000):
    a = isqrt(n) + 1
    for i in range(max_iter):
        b_sq = a * a - n
        b = isqrt(b_sq)
        if b * b == b_sq:
            p = a - b
            q = a + b
            if p * q == n:
                return p, q
        a += 1
    return None, None

def isqrt(n):
    if n < 2:
        return n
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

print("\nTrying Fermat factorization...")
p, q = fermat_factor(n, 1000000)

if p and q:
    print(f"Found factors!")
    print(f"p = {p}")
    print(f"q = {q}")
    
    # Decrypt
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    flag = long_to_bytes(m)
    print(f"\nFlag: {flag.decode()}")
else:
    print("Fermat didn't work quickly. Trying Coppersmith attack...")
    # We'll need to use sage for this
    print("\nLet me create a sage script for Coppersmith attack...")
