#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def adjust_key(key8: bytes) -> bytes:
    out = bytearray()
    for b in key8:
        b7 = b & 0xFE                
        ones = bin(b7).count("1")     
        out.append(b7 | (ones % 2 == 0))  
    return bytes(out)

# The vulnerability:
# v1: E_k1(E_k2(E_k3(pt)))
# v2: D_k1(E_k2(E_k3(pt)))
#
# If we have the same pt encrypted with both v1 and v2:
# v1_ct = E_k1(E_k2(E_k3(pt)))
# v2_ct = D_k1(E_k2(E_k3(pt)))
#
# Let X = E_k2(E_k3(pt))
# Then: v1_ct = E_k1(X) and v2_ct = D_k1(X)
# So: E_k1(v2_ct) = E_k1(D_k1(X)) = X
# And: D_k1(v1_ct) = D_k1(E_k1(X)) = X
#
# This means: E_k1(v2_ct) = D_k1(v1_ct)
# Or: E_k1(v2_ct) = D_k1(v1_ct)
#
# More importantly, since we control k2 and k3, we know X = E_k2(E_k3(pt))
# We can compute X for our plaintext, then:
# X = E_k1(v2_ct), so k1_encrypt(v2_ct) = X
# We can verify k1 candidates!
#
# But we still need to brute force k1...
# 
# WAIT! Even simpler: if we set k2 = k3 (but they check)
# What if we use DES weak keys or semi-weak keys?
#
# Actually, the REAL trick: Choose k2 and k3 such that E_k2(E_k3(x)) is easy to invert!
# We control both k2 and k3, so we can DECRYPT E_k2(E_k3(x))!
#
# For the flag:
# v2(flag) = D_k1(E_k2(E_k3(flag)))
# 
# If we can somehow get E_k1(v2(flag)), we get E_k2(E_k3(flag))
# Then we decrypt with k3 then k2 to get flag!
#
# But how do we apply E_k1? We don't know k1...
#
# AH! Use v1 on the v2 ciphertext!
# v1(v2(flag)) = E_k1(E_k2(E_k3(v2(flag))))
#
# Hmm, that's not quite right either...
#
# Let me think differently: 
# Choose k2 and k3, get v2(flag) = D_k1(E_k2(E_k3(flag)))
# We want to recover flag.
# 
# We can't get E_k1 directly, but we can use the oracle!
# If we encrypt v2(flag) with v1:
# v1(v2(flag)) = E_k1(E_k2(E_k3(D_k1(E_k2(E_k3(flag))))))
#
# Hmm, still complex...
#
# NEW IDEA: Use the ECB mode property!
# Since everything is ECB, we can mix and match blocks.
# But the flag is probably one block...
#
# ANOTHER IDEA: Use all zeros for k2 and k3!
# Wait, let's use k3 = all zeros, k2 = all ones (different)
# Then compute what we can...

conn = remote('20.193.149.152', 1340)

# Choose specific keys
# Let's use keys where we know the encryption behavior
k2_raw = bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01])
k3_raw = bytes([0xFE, 0xFE, 0xFE, 0xFE, 0xFE, 0xFE, 0xFE, 0xFE])

k2 = adjust_key(k2_raw)
k3 = adjust_key(k3_raw)

print(f"k2: {k2.hex()}")
print(f"k3: {k3.hex()}")

# Encrypt a known plaintext with v1
print("\n[*] Getting v1(known_pt)...")
conn.recvuntil(b'enter k2 hex bytes >')
conn.sendline(k2_raw.hex().encode())
conn.recvuntil(b'enter k3 hex bytes >')
conn.sendline(k3_raw.hex().encode())
conn.recvuntil(b'enter option >')
conn.sendline(b'2')  # v1
conn.recvuntil(b'enter option >')
conn.sendline(b'2')  # our own text
known_pt = pad(b'TESTTEST', 8)
conn.recvuntil(b'enter hex bytes >')
conn.sendline(known_pt.hex().encode())
conn.recvuntil(b'ciphertext : ')
v1_known = bytes.fromhex(conn.recvline().strip().decode())
print(f"v1(known_pt) = {v1_known.hex()}")

# Encrypt the same plaintext with v2
print("\n[*] Getting v2(known_pt)...")
conn.recvuntil(b'enter k2 hex bytes >')
conn.sendline(k2_raw.hex().encode())
conn.recvuntil(b'enter k3 hex bytes >')
conn.sendline(k3_raw.hex().encode())
conn.recvuntil(b'enter option >')
conn.sendline(b'3')  # v2
conn.recvuntil(b'enter option >')
conn.sendline(b'2')  # our own text
conn.recvuntil(b'enter hex bytes >')
conn.sendline(known_pt.hex().encode())
conn.recvuntil(b'ciphertext : ')
v2_known = bytes.fromhex(conn.recvline().strip().decode())
print(f"v2(known_pt) = {v2_known.hex()}")

# Now encrypt flag with v2
print("\n[*] Getting v2(flag)...")
conn.recvuntil(b'enter k2 hex bytes >')
conn.sendline(k2_raw.hex().encode())
conn.recvuntil(b'enter k3 hex bytes >')
conn.sendline(k3_raw.hex().encode())
conn.recvuntil(b'enter option >')
conn.sendline(b'3')  # v2
conn.recvuntil(b'enter option >')
conn.sendline(b'1')  # flag
conn.recvuntil(b'ciphertext : ')
v2_flag = bytes.fromhex(conn.recvline().strip().decode())
print(f"v2(flag) = {v2_flag.hex()}")

# Analysis:
# X_known = E_k2(E_k3(known_pt))
cipher2 = DES.new(k2, DES.MODE_ECB)
cipher3 = DES.new(k3, DES.MODE_ECB)
X_known = cipher2.encrypt(cipher3.encrypt(known_pt))
print(f"\nX_known = E_k2(E_k3(known_pt)) = {X_known.hex()}")

# We have: v1_known = E_k1(X_known) and v2_known = D_k1(X_known)
# So: D_k1(v1_known) = X_known and E_k1(v2_known) = X_known
print(f"v1_known should equal E_k1(X_known): {v1_known.hex()}")
print(f"v2_known should equal D_k1(X_known): {v2_known.hex()}")

# Now I can brute force k1! DES has 2^56 keys, but with parity it's 2^64 bytes
# This is too much for brute force in reasonable time...
# 
# Wait, maybe there's a weak key involved? Or maybe I'm missing something simpler?

conn.close()

print("\n[!] Need to think about this more...")
print("[!] The meet-in-the-middle attack might work but requires significant computation")
