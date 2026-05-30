# -*- coding: utf-8 -*-

# solve.sage (ASCII-safe)
# Recover secret polynomial key from (z,w) and decrypt AES ECB

from sage.all import *
from sage.modules.free_module_integer import IntegerLattice
import hashlib

print("[*] Reading ciphertext.txt ...")
with open("ciphertext.txt", "r") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

if len(lines) < 2:
    raise RuntimeError("ciphertext.txt must contain at least 2 lines")

key_enc_str = lines[0]
ct_hex = lines[1]

print("[*] key_enc line:")
print(key_enc_str)
print("[*] ciphertext hex:")
print(ct_hex)

# Ring Z[x]/(x^256+1)
n = 256
R.<x> = ZZ['x']
P.<a> = R.quotient(x^n + 1)

# Parse "(z , w)"
if not (key_enc_str[0] == '(' and key_enc_str[-1] == ')'):
    raise RuntimeError("key_enc format error")

body = key_enc_str[1:-1]
comma_idx = body.find(',')
if comma_idx == -1:
    raise RuntimeError("Missing comma in key_enc")

z_str = body[:comma_idx].strip()
w_str = body[comma_idx+1:].strip()

print("[*] Parsed z_str:")
print(z_str)
print("[*] Parsed w_str:")
print(w_str)

z = P(z_str)
w = P(w_str)

poly_z = z.lift()
poly_w = w.lift()

def coeff_vec(poly, n=256):
    return [ZZ(poly[i]) for i in range(n)]

z_coeffs = coeff_vec(poly_z, n)
w_coeffs = coeff_vec(poly_w, n)

print("[*] Got coefficient vectors for z, w")

# Use equations z_k = (e*w)_k for k >= 75
rows_idx = list(range(75, n))
m = len(rows_idx)
print("[*] Using %d equations (k from 75 to 255)" % m)

A = Matrix(ZZ, m, n)

print("[*] Building matrix A ...")
for j in range(n):
    if j % 32 == 0:
        print("    column %d / %d" % (j, n))
    e_poly = a^j
    prod = (e_poly * w).lift()
    for ri, k in enumerate(rows_idx):
        A[ri, j] = ZZ(prod[k])

b = vector(ZZ, [z_coeffs[k] for k in rows_idx])

print("[*] Matrix A size: %d x %d" % (A.nrows(), A.ncols()))

# Build lattice basis: vectors v_j = (e_j-block, A[:,j]-block)
print("[*] Building lattice basis ...")
basis_rows = []
for j in range(n):
    row = [ZZ(0)] * (n + m)
    row[j] = ZZ(1)
    for ri in range(m):
        row[n + ri] = A[ri, j]
    basis_rows.append(row)

M = Matrix(ZZ, basis_rows)
print("[*] Lattice dimension: %d x %d" % (M.nrows(), M.ncols()))

# Target t = (0, b)
L = IntegerLattice(M)
t = vector(ZZ, [ZZ(0)]*n + list(b))

print("[*] Running closest_vector ...")
v_close = L.closest_vector(t)
print("[*] closest_vector done")

e_candidate = [ZZ(v_close[i]) for i in range(n)]

print("[*] Candidate e (first 20):")
print(e_candidate[:20])

max_abs_e = max(abs(c) for c in e_candidate)
print("[*] max |e_i| = %d" % max_abs_e)

# Verify e*w reproduces z for k>=75
print("[*] Verifying ...")
e_poly = sum(e_candidate[i] * a^i for i in range(n))
prod_ew = (e_poly * w).lift()
prod_coeffs = coeff_vec(prod_ew, n)

ok = True
for k in rows_idx:
    if prod_coeffs[k] != z_coeffs[k]:
        print("Mismatch at k=%d" % k)
        ok = False
        break

if ok:
    print("[+] High-degree checks passed")
else:
    print("[!] WARNING: High-degree checks failed")

# AES decrypt
print("[*] Decrypting AES ...")
key_poly = e_poly
key_str = str(key_poly)

key_hash = hashlib.sha256(key_str.encode()).digest()
key_aes = key_hash[:16]

print("[*] AES key (hex) =", key_aes.hex())

ct = bytes.fromhex(ct_hex)

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    cipher = AES.new(key_aes, AES.MODE_ECB)
    pt = cipher.decrypt(ct)
    try:
        pt_unpadded = unpad(pt, 16)
    except:
        pt_unpadded = pt
    print("[+] Plaintext raw:", pt_unpadded)
    try:
        print("[+] UTF8:", pt_unpadded.decode())
    except:
        pass
except ImportError:
    print("[!] Python Crypto not installed. Use external AES tool.")
