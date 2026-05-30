#!/usr/bin/env python3
import hashlib, os, urllib.request
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fpylll import IntegerMatrix, LLL
from skyfield.api import Loader
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN

# --- Output data ---
p          = 10035410270612815279389330410121900529620495869479898461384631211745452304638984576440553552006414411373806160282016417372459090604747980402493134112626213
STEPS      = [0, 4, 10, 18, 28]
TRUNC      = [1129223615711367884405014640005288172041367198689786688285,
              579514026315281536883405991880758556036404753274817543322,
              1279648546218423539959079224022586160480305721841176089544,
              1946366015289015629063708515503091199628321083313573104031,
              3902208990133988884490762855871313599751888895643028675415]
iv         = bytes.fromhex("ba04a327ffd0c69205ff5dcb5f463d9c")
ciphertext = bytes.fromhex("1879e4d0f174c9a6d2be99b6f632cc0f3ea89989e69dbd080761cb616b37d8eba37635de6c6475d741f69450c8259590")
EPOCH_HASH = bytes.fromhex("8b156702c993b9b5")
UBITS      = 320  # unknown lower bits per LCG state

# --- Step 1: Recover epoch time by brute-force ---
epoch_time = next(
    (hh, mm, ss)
    for hh in range(24) for mm in range(60) for ss in range(60)
    if hashlib.sha256(f"{hh:02d}:{mm:02d}:{ss:02d}".encode()).digest()[:8] == EPOCH_HASH
)
print(f"[+] Epoch time: {epoch_time[0]:02d}:{epoch_time[1]:02d}:{epoch_time[2]:02d}")

# --- Step 2: Derive LCG params a, b from Halley's comet position ---
load = Loader('/tmp/skyfield-data')
os.makedirs("/tmp/skyfield-data", exist_ok=True)
comet_file = "/tmp/skyfield-data/CometEls.txt"
if not os.path.exists(comet_file):
    urllib.request.urlretrieve(
        "https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft00Cmt.txt", comet_file)

with open(comet_file, "rb") as f:
    row = mpc.load_comets_dataframe(f).set_index('designation', drop=False).loc['1P/Halley']

ts  = load.timescale()
t   = ts.utc(2026, 1, 26, *epoch_time)
sun = load('de421.bsp')['sun']
pos = sun.at(t).observe(sun + mpc.comet_orbit(row, ts, GM_SUN)).position.au
coord_str = f"{pos[0]:.10f}_{pos[1]:.10f}_{pos[2]:.10f}"
a = bytes_to_long(hashlib.sha512((coord_str + "_A").encode()).digest())
b = bytes_to_long(hashlib.sha512((coord_str + "_B").encode()).digest())
print("[+] Derived a, b from comet position")

# --- Step 3: Kannan embedding + LLL to recover LCG initial state ---
# s_k = A[k]*s_0 + B[k] (mod p), top 192 bits known, bottom 320 unknown
inv_a1 = pow(a - 1, -1, p)
A = [pow(a, s, p) for s in STEPS]
B = [0 if s == 0 else (b * (A[i] - 1) * inv_a1) % p for i, s in enumerate(STEPS)]
h = [t << UBITS for t in TRUNC]  # known high parts
D = [(A[i] * h[0] + B[i] - h[i]) % p for i in range(1, 5)]

K = 1 << UBITS
lattice = [
    [1, A[1], A[2], A[3], A[4], 0],
    [0,    p,    0,    0,    0, 0],
    [0,    0,    p,    0,    0, 0],
    [0,    0,    0,    p,    0, 0],
    [0,    0,    0,    0,    p, 0],
    [0, D[0], D[1], D[2], D[3], K],
]
M = IntegerMatrix(6, 6)
for i, row_data in enumerate(lattice):
    for j, val in enumerate(row_data):
        M[i, j] = int(val)

print("[*] Running LLL...")
LLL.reduction(M)

s0 = None
for i in range(6):
    if abs(M[i][5]) == K:
        sign = 1 if M[i][5] == K else -1
        e0 = sign * M[i][0]
        if 0 <= e0 < K:
            s0_cand = h[0] + e0
            if all((A[j] * s0_cand + B[j]) % p >> UBITS == TRUNC[j] for j in range(1, 5)):
                s0 = s0_cand
                break

if s0 is None:
    raise RuntimeError("Lattice attack failed")

# --- Step 4: Advance to final_state and decrypt ---
final_state = (a * (A[4] * s0 + B[4]) % p + b) % p
aes_key     = hashlib.sha256(long_to_bytes(final_state)).digest()
flag        = unpad(AES.new(aes_key, AES.MODE_CBC, iv).decrypt(ciphertext), 16)
print(f"\n[+] FLAG: {flag.decode()}")
