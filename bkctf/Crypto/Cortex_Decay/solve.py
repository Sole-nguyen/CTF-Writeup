from Crypto.Util.number import long_to_bytes

# The challenge parameters
c = 40732687938760268194816992508783308058844901710443215136378413744389173154801
e = 65537
n = 67000000000000000000000000245061662851489575612371642903203727663237160203426

# n is a multi-prime RSA modulus with 8 prime factors (easily factorable)
# Factors found via trial division + factordb
primes = [2, 3, 67, 1483, 14180303, 40938258341, 1324437742957822811, 146170986161787706448601731202221987]

# phi(n) = product of (p-1) for all prime factors
phi = 1
for p in primes:
    phi *= (p - 1)

d = pow(e, -1, phi)
m = pow(c, d, n)

flag = long_to_bytes(m)
print(f"Flag: {flag.decode('utf-8')}")
