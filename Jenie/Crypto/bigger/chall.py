#!/usr/bin/env python3

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes, GCD
from secret import FLAG

"""
I heard about RSA key length which needs now to be at least 4096 to be secure...
To be sure nobody will read my secret message, I will use a bigger key ;)
"""

e = 78676413582343569846949828607 # our homemade public exponent

# N = p*q so, 96 * 96 = 9216 key length, very secure
p = getPrime(96)
q = getPrime(96)

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

N = p * q

pt = bytes_to_long(FLAG)
ct = pow(pt, e, N)

print(f"N = {N}")
print(f"e = {e}")
print(f"The secret message is: {ct}")

pt = pow(ct, d, N)
decrypted = long_to_bytes(pt)

assert decrypted == FLAG
