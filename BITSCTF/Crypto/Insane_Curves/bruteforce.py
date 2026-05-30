#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

# Given from analysis: p+1 is extremely smooth!
# p+1 = 2^23 * 3^14 * 5^8 * 7^4 * 11^10 * 13^10 * 17^9 * 19^6 * 23^5 * 29 * 31^4

# For genus 2, #J(F_p) ~ (p+1)^2 by Hasse-Weil bound
# Since p+1 is smooth, #J is likely smooth -> Pohlig-Hellman will work

# But first, let me check if there's a simpler attack
# Since f factors completely, maybe we can use a meet-in-the-middle or Baby-step Giant-step
# with smaller search space

# Actually, wait - let me try bruteforcing small values of k
# If the challenge is solvable, k might be small

enc_flag = bytes.fromhex("f6ca1f88bdb8e8dda17861b91704523f914564888c7138c24a3ab98902c10de5")

print("[+] Trying small values of k...")

def is_printable(data):
    try:
        decoded = data.decode('ascii')
        return all(32 <= ord(c) < 127 for c in decoded)
    except:
        return False

for k in range(1, 10000000):
    key = hashlib.sha256(long_to_bytes(k)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        plaintext = cipher.decrypt(enc_flag)
        # Check if it's printable ASCII 
        if is_printable(plaintext):
            print(f"\n[+] Found printable output with k={k}!")
            print(f"[+] Plaintext: {plaintext}")
            print(f"[+] Decoded: {plaintext.decode('ascii')}")
            if b'BITS' in plaintext or b'flag' in plaintext or b'{' in plaintext:
                print(f"[!!!] This looks like the flag!")
                break
    except:
        pass
    
    if k % 1000000 == 0:
        print(f"[+] Tried {k} values...")

print("\n[+] Done brute force")
