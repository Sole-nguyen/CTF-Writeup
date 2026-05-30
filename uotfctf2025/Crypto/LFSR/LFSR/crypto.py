import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def derive_key(state_bits, length=32):
    data = bytes(state_bits)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=length, salt=None, info=b"nlfg-ctf")
    return hkdf.derive(data)


def encrypt(flag: bytes, state_bits):
    key = derive_key(state_bits, length=32)
    nonce = os.urandom(12)
    aead = ChaCha20Poly1305(key)
    ct = aead.encrypt(nonce, flag, associated_data=None)
    return nonce, ct


def decrypt(nonce, ct, state_bits):
    key = derive_key(state_bits, length=32)
    aead = ChaCha20Poly1305(key)
    return aead.decrypt(nonce, ct, associated_data=None)

