import json
import numpy as np
import hashlib
from fpylll import IntegerMatrix, LLL, BKZ

# ── Load challenge data ────────────────────────────────────────────────────────
with open('challenge_data.json') as f:
    data = json.load(f)

q      = data['q']        # 12289
n      = data['n']        # 512
A_raw  = data['A']        # 512×512 rotation matrix of h (cyclotomic)
hints  = data['hints']    # 436 pairs [index, f[index]]

A = np.array(A_raw, dtype=np.int64)

# ── Parse known / unknown indices ──────────────────────────────────────────────
f_known = {idx: val for idx, val in hints}
known_set = set(f_known)
unknown_indices = [i for i in range(n) if i not in known_set]
m = len(unknown_indices)   # 76
print(f"[*] Known f coefficients: {len(f_known)}, Unknown: {m}")

# ── Compute c_mod[j] = (Σ_{i∈K} f[i]·A[i][j]) mod q ─────────────────────────
print("[*] Computing c_mod ...")
c_mod = np.zeros(n, dtype=np.int64)
for i, val in f_known.items():
    c_mod += val * A[i]
c_mod = c_mod % q

# Centre to [-q//2, q//2]
c_cent = np.where(c_mod > q // 2, c_mod - q, c_mod).tolist()

# ── Build a smaller (2m+1 = 153) Kannan lattice using only m equations ────────
#
#  Choose m "equation" columns J ⊂ {0..n-1}.
#  Relation: f_U · A_U_J  ≡  g_J - c_mod_J  (mod q)
#  where A_U_J is the m×m submatrix of A (rows=unknown f indices, cols=J).
#
#  Kannan lattice (dim = 2m+1):
#    rows 0..m-1   : [ e_k^m | A_U_J[k,:] | 0 ]
#    rows m..2m-1  : [ 0^m   | q·e_j^m    | 0 ]
#    last row      : [ 0^m   | c_cent_J   | 1 ]  (Kannan target)
#
#  Short vector (f_U, g_J, ±1) has norm ≈ sqrt(76*16 + 76*16 + 1) ≈ 49.
#
eq_indices = list(range(m))   # use first m=76 columns as equations
A_U = A[np.array(unknown_indices), :]         # m × n
A_U_J = A_U[:, eq_indices]                   # m × m
c_cent_J = [c_cent[j] for j in eq_indices]

print(f"[*] Building {2*m+1}×{2*m+1} Kannan lattice ...")
dim = 2 * m + 1
mat = [[0] * dim for _ in range(dim)]

for k in range(m):                            # f_U basis rows
    mat[k][k] = 1
    for j in range(m):
        mat[k][m + j] = int(A_U_J[k, j])

for j in range(m):                            # mod-q rows
    mat[m + j][m + j] = q

for j in range(m):                            # Kannan target row
    mat[2 * m][m + j] = c_cent_J[j]
mat[2 * m][2 * m] = 1

# ── LLL reduction ─────────────────────────────────────────────────────────────
print("[*] Running LLL + progressive BKZ ...")
IM = IntegerMatrix.from_matrix(mat)
LLL.reduction(IM)
# Progressive BKZ: block_size 10→20→30, 5 loops each
for bs in [10, 20, 30]:
    BKZ.reduction(IM, BKZ.Param(block_size=bs, flags=BKZ.AUTO_ABORT | BKZ.MAX_LOOPS, max_loops=5))
print("[*] BKZ done.")

# ── Extract the short vector ──────────────────────────────────────────────────
def find_solution(IM, m, threshold=50):
    dim = 2 * m + 1
    for i in range(dim):
        last = IM[i][2 * m]
        if abs(last) != 1:
            continue
        sign = last
        x_cand = [sign * IM[i][k]     for k in range(m)]
        y_cand = [sign * IM[i][m + k] for k in range(m)]
        if max(abs(v) for v in x_cand) < threshold and max(abs(v) for v in y_cand) < threshold:
            return x_cand, y_cand
    return None

solution = find_solution(IM, m)

if solution is None:
    print("[-] No clean solution found. Candidates with |last|==1:")
    for i in range(2 * m + 1):
        if abs(IM[i][2 * m]) == 1:
            x_c = [IM[i][k] for k in range(m)]
            y_c = [IM[i][m + k] for k in range(m)]
            print(f"  row {i}: max|x|={max(abs(v) for v in x_c)}, max|y|={max(abs(v) for v in y_c)}")
    raise RuntimeError("Could not recover f_U")

f_U_vals, g_J_vals = solution
print(f"[+] Found: max|f_U|={max(abs(v) for v in f_U_vals)}, max|g_J|={max(abs(v) for v in g_J_vals)}")

# ── Reconstruct full f ────────────────────────────────────────────────────────
f_full = [0] * n
for ki, val in f_known.items():
    f_full[ki] = val
for idx, ui in enumerate(unknown_indices):
    f_full[ui] = f_U_vals[idx]

print(f"[*] f_full — max: {max(f_full)}, min: {min(f_full)}, "
      f"||f||={sum(v**2 for v in f_full)**0.5:.1f}")

# ── Full sanity check: verify f·A ≡ g (mod q) with small g ───────────────────
f_np_check = np.array(f_full, dtype=np.int64)
g_full = (f_np_check @ A) % q
g_cent = np.where(g_full > q // 2, g_full - q, g_full)
print(f"[*] Recovered g — max: {int(g_cent.max())}, min: {int(g_cent.min())}, "
      f"||g||={float(np.linalg.norm(g_cent)):.1f}")
if g_cent.max() < 100 and g_cent.min() > -100:
    print("[+] Sanity check passed (g is small).")
else:
    print("[-] WARNING: g coefficients are large. f may be wrong.")

# ── Decrypt the flag ──────────────────────────────────────────────────────────
encrypted = bytes.fromhex(open('challenge_flag.enc').read().strip())

for dtype in [np.int64, np.int32]:
    f_np  = np.array(f_full, dtype=dtype)
    key   = hashlib.sha256(f_np.tobytes()).digest()
    flag  = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted)])
    if flag.startswith(b'BITSCTF{'):
        print(f"[+] FLAG ({dtype.__name__}): {flag.decode()}")
        break
    print(f"[-] dtype={dtype.__name__} did not yield flag. Raw: {flag[:20]}")
