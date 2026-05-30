# pip install pycryptodome sympy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from sympy import randprime, nextprime

from secret import FLAG

p = randprime(1<<1023, 1<<1024)
q = nextprime(p)
n = p * q
e = 0x10001

pub_key = RSA.construct((n, e))
print(pub_key.export_key().decode(), end="\n\n")

cipher = PKCS1_OAEP.new(pub_key)
ciphertext = cipher.encrypt(FLAG)
print("Encrypted:", ciphertext.hex())