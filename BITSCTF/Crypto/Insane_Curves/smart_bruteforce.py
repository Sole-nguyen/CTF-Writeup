#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

enc_flag = bytes.fromhex("f6ca1f88bdb8e8dda17861b91704523f914564888c7138c24a3ab98902c10de5")

print("[+] Maybe the private key is small or has special structure...")
print("[+] Trying common patterns...")

def try_decrypt(k):
    key = hashlib.sha256(long_to_bytes(k)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(enc_flag)
    return plaintext

def is_flag(data):
    try:
        s = data.decode('ascii')
        return 'BITS{' in s or 'FLAG{' in s or 'flag{' in s
    except:
        return False

# Try small values first
print("\n[+] Trying small values 1-100000...")
for k in range(1, 100001):
    pt = try_decrypt(k)
    if is_flag(pt):
        print(f"\n[!!!] FOUND FLAG with k={k}!")
        print(f"[!!!] FLAG: {pt.decode('ascii')}")
        exit(0)

# Try powers and special numbers
print("\n[+] Trying special values...")
special_vals = [
    2**16, 2**20, 2**24, 2**32,
    1337, 31337, 13**37,
    0xdeadbeef, 0xcafebabe, 0x1337,
    123456789, 987654321,
    42, 1234, 12345, 123456
]

for k in special_vals:
    pt = try_decrypt(k)
    if is_flag(pt):
        print(f"\n[!!!] FOUND FLAG with k={k}!")
        print(f"[!!!] FLAG: {pt.decode('ascii')}")
        exit(0)

# Since p+1 is 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4
# Maybe k is one of the small prime factors or combinations?
print("\n[+] Trying products of small smooth factors...")
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

for p1 in primes:
    for exp1 in range(1, 10):
        k = p1**exp1
        if k > 10**10:
            break
        pt = try_decrypt(k)
        if is_flag(pt):
            print(f"\n[!!!] FOUND FLAG with k={k}={p1}^{exp1}!")
            print(f"[!!!] FLAG: {pt.decode('ascii')}")
            exit(0)

# Try combinations of two primes
for i, p1 in enumerate(primes):
    for j, p2 in enumerate(primes):
        if j <= i:
            continue
        for e1 in range(1, 6):
            for e2 in range(1, 6):
                k = (p1**e1) * (p2**e2)
                if k > 10**12:
                    break
                pt = try_decrypt(k)
                if is_flag(pt):
                    print(f"\n[!!!] FOUND FLAG with k={k}={p1}^{e1}*{p2}^{e2}!")
                    print(f"[!!!] FLAG: {pt.decode('ascii')}")
                    exit(0)

print("\n[-] No flag found in searched space")
