import json
from hashlib import sha256
from Crypto.Cipher import AES

# --- Load and Setup ---
with open('output.json', 'r') as f:
    data = json.load(f)

Q = data['spec']['q']
M = data['spec']['m']
N = data['spec']['n']
K = data['spec']['k']

R.<x> = PolynomialRing(GF(Q))
MODPOLY = R(data['spec']['modulus'])
Fq = GF(Q)
Fqm.<a> = GF(Q**M, modulus=MODPOLY)

def unpack_elem(val):
    val = int(val)
    bits = [(val >> i) & 1 for i in range(M)]
    return Fqm(bits)

def unpack_vec(v):
    return vector(Fqm, [unpack_elem(x) for x in v])

def unpack_mat(mat):
    return Matrix(Fqm, [[unpack_elem(x) for x in row] for row in mat])

warp = unpack_mat(data['warp'])
bolt = unpack_vec(data['bolt'])
pegs = unpack_vec(data['loom']['pegs'])
knot = unpack_mat(data['loom']['knot'])
shuttle = unpack_mat(data['loom']['shuttle'])

# Calculate the target vector
y = bolt * shuttle

# --- Gabidulin Decoding (Berlekamp-Welch Approach) ---
# We find a linearized error-locator polynomial Lambda(x) of degree 15 
# and a polynomial N(x) = Lambda(S(x)) of degree 15 + 7 = 22.
num_n = 23
num_l = 15
eqs = []
rhs = []

# Build the linear system: N(p_j) - Lambda(y_j) = 0
for j in range(N):
    pj = pegs[j]
    yj = y[j]
    row = []
    
    # n_i coefficients
    for i in range(num_n):
        row.append(pj**(2**i))
        
    # lambda_i coefficients (lambda_15 is fixed to 1, moved to RHS)
    for i in range(num_l):
        row.append(-yj**(2**i))
        
    eqs.append(row)
    rhs.append(yj**(2**15))

M_sys = Matrix(Fqm, eqs)
v_rhs = vector(Fqm, rhs)
sol = M_sys.solve_right(v_rhs)

n_coeffs = sol[:num_n]
lambda_coeffs = list(sol[num_n:]) + [Fqm(1)]

# Find the lowest non-zero index in Lambda to safely compute S(x)
z = 0
while lambda_coeffs[z] == Fqm(0):
    z += 1

# Iteratively extract the coefficients of S(x) (which is s_prime)
s_prime = []
for k in range(K):
    val = n_coeffs[k + z]
    for i in range(z + 1, min(k + z, 15) + 1):
        if k + z - i < len(s_prime):
            val -= lambda_coeffs[i] * (s_prime[k + z - i]**(2**i))
    # Root finding in GF(2^M): X^(2^z) = Y  =>  X = Y^(2^(M-z))
    s_prime.append((val / lambda_coeffs[z])**(2**(M - z)))

s_prime_vec = vector(Fqm, s_prime)

# secret * knot = s_prime => secret = s_prime * knot^-1
secret = s_prime_vec * knot.inverse()

# --- Unpack and Decrypt ---
def pack(v):
    out = []
    for e in v:
        cs = list(e.polynomial()) if e else []
        cs = [int(c) for c in cs] + [0] * (M - len(cs))
        val = 0
        for i, c in enumerate(cs):
            val |= c << i
        out.append(int(val))
    return out

secret_packed = pack(secret)
secret_bytes = b''.join(int(v).to_bytes((M + 7) // 8, 'big') for v in secret_packed)
wrap_key = sha256(secret_bytes).digest()[:16]

iv = bytes.fromhex(data['vault']['iv'])
body = bytes.fromhex(data['vault']['body'])
tag = bytes.fromhex(data['vault']['tag'])

cipher = AES.new(wrap_key, AES.MODE_GCM, nonce=iv)
flag = cipher.decrypt_and_verify(body, tag)

print(f"[*] Decrypted Flag: {flag.decode('utf-8')}")