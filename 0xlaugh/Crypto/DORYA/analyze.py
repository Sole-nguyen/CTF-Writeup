"""
Analysis of the Möbius transformation:
f(m) = (a*m + b) / (c*m + d) mod n

After each round, coefficients change:
a += 2^1024
b += 4^1024 = 2^2048
c += 6^1024
d += 8^1024 = 2^3072

Initial: a=2^1024, b=3*2^1024, c=3*2^1024, d=7*2^1024

The key insight: As coefficients grow, what happens to the transformation?

Let me check the relationship between consecutive rounds...
"""

# Initial coefficients
a_0 = 1 * 2**1024
b_0 = 3 * 2**1024
c_0 = 3 * 2**1024
d_0 = 7 * 2**1024

print("Initial coefficients:")
print(f"a_0 / 2^1024 = 1")
print(f"b_0 / 2^1024 = 3")
print(f"c_0 / 2^1024 = 3")
print(f"d_0 / 2^1024 = 7")
print()

# Compute coefficients for each round
for i in range(7):
    a = a_0 + i * 2**1024
    b = b_0 + i * 4**1024
    c = c_0 + i * 6**1024
    d = d_0 + i * 8**1024
    
    print(f"Round {i}:")
    print(f"  a / 2^1024 = {a // 2**1024}")
    print(f"  b / 2^2048 = {b // 2**2048}")
    print(f"  c / 2^1024 = {c // 2**1024} (but c has large component from 6^1024)")
    print(f"  d / 2^3072 = {d // 2**3072}")
    
    # Check magnitudes
    import math
    print(f"  log2(a) ≈ {int(math.log2(a))}")
    print(f"  log2(b) ≈ {int(math.log2(b))}")
    print(f"  log2(c) ≈ {int(math.log2(c))}")
    print(f"  log2(d) ≈ {int(math.log2(d))}")
    print()

print("\nKey observation:")
print("b, c, and d grow much faster than a!")
print("b has 4^1024 term, c has 6^1024 term, d has 8^1024 term")
print("So as rounds progress, the transformation becomes dominated by these large terms.")
print()
print("4^1024 = 2^2048")
print(f"6^1024 ≈ 2^{int(1024 * math.log2(6))}")
print(f"8^1024 = 2^{3072}")
