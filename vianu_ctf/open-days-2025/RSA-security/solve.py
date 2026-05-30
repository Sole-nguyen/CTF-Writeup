from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import gmpy2

public_key_pem = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk9Lh/XH/MSssW0TnIDaw
NQg3gaoSBsB33JKLm4Y8iduZkUk4xnhi7q1jk69cwDJ5fcCmVnb19q3EAbl/tMi3
KXexlSnWoBjJGbXNATrQYITBWX3UuwAXGhZm55wVGxcDRkzD6WDtyrPEfLXAobVB
AB7DXliy9NEb7WEkQ1qSvyfzLREWXzocSggbuC3suxL0q2rqM/pZLrzeZoAD79QA
mUx4MWc23L7vqkxRtUe/X+idtaMuNbgazS5g5ND/Rnndd6B7tmLULUUMp7eQWTl6
phfKqEgOwV0ifn8qt9yL4JyEjIm+A3/kT+gTmhTB0xmqnmvoGt30Mn9Af+nUqSYN
LwIDAQAB
-----END PUBLIC KEY-----"""

ciphertexthex = "51523fd876a3041e6a62f4f318700d31362ae4e750d56a7d1f734e74e9c9d1c531e4a5d886bb5cc40b80005c4f13dd342a3e44b20741c72b51cd6036ee54f8077e681492cfff52e9993fb3c6bd3639de1c2cf4097a8009a9f79616c0da304e579c7aabb4fc906501aba62261fadf4d7f97facd428cf1b226bc6cf69e9164ea62085f32ee8d866c6f9a379a09ee97b0a1acce80536ee29de43e7650f91e1e399ded212813e2764fe6e4e6ac7ed4e1d209bf82cd2ce0655f05d4e455e23625513c4ac17fd053f3a888c5cb2b89b0f5268a7e2de5396a023aed9a41a2859f19537bd30bb978e5e113cc1ba90f60276caabe5eff135f16942b7107a99ed81f55bbb4"
ciphertext = bytes.fromhex(ciphertexthex)

pub_key = RSA.import_key(public_key_pem)
n = pub_key.n
e = pub_key.e

def fermat_factorization(n):
    a = gmpy2.isqrt(n)
    if a*a < n:
        a += 1
    
    while True:
        b2 = a*a - n
        if gmpy2.is_square(b2):
            b = gmpy2.isqrt(b2)
            p = a - b
            q = a + b
            return int(p), int(q)
        a += 1

p, q = fermat_factorization(n)
print(f"p: {p}")
print(f"q: {q}")

phi = (p - 1) * (q - 1)
d = int(gmpy2.invert(e, phi))

priv_key = RSA.construct((n, e, d, p, q))
cipher = PKCS1_OAEP.new(priv_key)
flag = cipher.decrypt(ciphertext)
print(flag.decode())