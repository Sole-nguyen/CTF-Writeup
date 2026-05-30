from sage.all import *
import json
import hashlib

with open("output.txt", "r") as f:
    data = json.load(f)

q = data["q"]
A = Matrix(ZZ, data["A"])
b = vector(ZZ, data["b"])
Bs = Matrix(ZZ, data["Bs"])
enc_flag = bytes.fromhex(data["enc_flag_hex"])

n = 40
m = 60

BsA = Bs * A

lat_rows = []

for i in range(m):
    row = [0] * (m + n)
    row[i] = q
    lat_rows.append(row)

for i in range(n):
    row = [0] * (m + n)
    for j in range(m):
        row[j] = int(BsA[i, j])
    row[m + i] = 1
    lat_rows.append(row)

for j in range(m):
    lat_rows[j][j] = q

L = Matrix(ZZ, lat_rows)

target = list(b) + [0] * n

L_red = L.LLL()
G = L_red.gram_schmidt()[0]

t = vector(ZZ, target)
w = t
for i in range(L_red.nrows() - 1, -1, -1):
    w = w - round((w * G[i]) / (G[i] * G[i])) * L_red[i]

v = t - w

z_part = v[m:m+n]

if all(abs(x) <= 1 for x in z_part):
    z = vector(ZZ, z_part)
    s = (z * Bs) % q
    
    check = (s * A) % q
    err = [(check[j] - b[j]) % q for j in range(m)]
    err = [e if e < q//2 else e - q for e in err]
    max_err = max(abs(e) for e in err)
    
    if max_err <= 10:
        key = hashlib.sha256(b"".join(int(s[k]).to_bytes(2, "little") for k in range(n))).digest()
        flag = bytes(enc_flag[k] ^ key[k % len(key)] for k in range(len(enc_flag)))
        print(flag.decode())
