# -*- coding: utf-8 -*-
from sage.all import *
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

print("[*] Loading ciphertext.txt ...")

raw = open("ciphertext.txt").read().strip()

# ============================================================
# PARSE (z, w)
# ============================================================

m = re.search(r"\((.*)\)", raw, flags=re.DOTALL)
inside = m.group(1).strip()

depth = 0
split_pos = -1
for i,ch in enumerate(inside):
    if ch == '(':
        depth += 1
    elif ch == ')':
        depth -= 1
    elif ch == ',' and depth == 0:
        split_pos = i
        break

z_str = inside[:split_pos].strip()
w_str = inside[split_pos+1:].strip()

# Convert ^ → **
def fix_power(s):
    return re.sub(r"\^(\d+)", r"**\1", s)

z_str = fix_power(z_str)
w_str = fix_power(w_str)

# ============================================================
# PARSE ciphertext hex
# ============================================================

m2 = re.search(r"([0-9a-fA-F]{40,})$", raw)
ct_hex = m2.group(1).strip()

print("[+] Ciphertext hex:", ct_hex)

# ============================================================
# BUILD polynomial ring
# ============================================================

n = 256

Rt.<t> = PolynomialRing(ZZ)
P.<a> = QuotientRing(Rt, t**n + 1)

z = eval(z_str, {"a": a})
w = eval(w_str, {"a": a})

print("[+] Parsed z, w in Sage.")

# ============================================================
# CORRECT coeff extractor
# ============================================================

def coeffs(poly):
    rep = poly.lift()        # in ZZ[t]
    rep = rep % (t**n + 1)   # reduce correctly
    return [ZZ(rep[i]) for i in range(n)]

zv = coeffs(z)
wv = coeffs(w)

print("[+] Coeff extraction OK.")

# ============================================================
# BUILD linear system A*e = b  (rows 75..255)
# ============================================================

rows = list(range(75,256))

def mult_column(j):
    tmp = [0]*n
    for i in range(n):
        if wv[i] == 0: continue
        idx = i + j
        if idx >= n:
            tmp[idx-n] -= wv[i]
        else:
            tmp[idx] += wv[i]
    return tmp

A = Matrix(QQ, len(rows), n)
for col in range(n):
    colv = mult_column(col)
    for r_i,k in enumerate(rows):
        A[r_i,col] = colv[k]

b = vector(QQ, [zv[k] for k in rows])

print("[*] Solving A*e = b ...")

e = A.solve_right(b)
e_int = [ZZ(round(v)) for v in e]

print("[+] First 10 coefficients:", e_int[:10])

# ============================================================
# RECONSTRUCT KEY
# ============================================================

key_poly = sum(e_int[i]*a**i for i in range(n))

print("[+] Key reconstructed.")

# ============================================================
# AES decrypt
# ============================================================

key_aes = sha256(str(key_poly).encode()).digest()[:16]
cipher = AES.new(key_aes, AES.MODE_ECB)
pt_raw = cipher.decrypt(bytes.fromhex(ct_hex))

try:
    pt = unpad(pt_raw, 16)
except:
    pt = pt_raw

print("\n================ FLAG ================\n")
print(pt)
print("\n======================================\n")
