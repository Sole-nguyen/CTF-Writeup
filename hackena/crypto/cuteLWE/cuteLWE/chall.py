from sage.all import *
import json, hashlib
from random import randint

FLAG = b"Hackena{Local_flag_FTW}"
q, n, k, m = 12289, 40, 12, 60
F = GF(q)

def rand_nonzero_vector(L, a, b):
    v = [randint(a, b) for _ in range(L)]
    while not any(v):
        v = [randint(a, b) for _ in range(L)]
    return vector(ZZ, v)

def random_nonsingular_matrix(field, dim, q):
    M = Matrix(field, dim, dim, lambda i, j: randint(0, q - 1))
    while M.is_singular():
        M = Matrix(field, dim, dim, lambda i, j: randint(0, q - 1))
    return M

def to_int_matrix(M):
    return [[int(x) for x in row] for row in M.rows()]

def main():
    A = Matrix(F, n, m, lambda i, j: randint(0, q - 1))
    H0 = random_nonsingular_matrix(F, k, q)
    H1 = Matrix(F, n - k, k, lambda i, j: randint(0, q - 1))
    Xf = -(H1 * H0.inverse())
    X = Matrix(ZZ, n - k, k, lambda i, j: int(Xf[i, j]))
    Bs = block_matrix([
        [q * identity_matrix(ZZ, k), zero_matrix(ZZ, k, n - k)],
        [X, identity_matrix(ZZ, n - k)],
    ])

    z = rand_nonzero_vector(n, -1, 1)
    s = vector(F, [int(x) % q for x in (z * Bs)])
    e = rand_nonzero_vector(m, -1, 1)
    b = (s * A) + vector(F, [int(e[i]) % q for i in range(m)])

    key = hashlib.sha256(b"".join(int(s[i]).to_bytes(2, "little") for i in range(n))).digest()
    enc = bytes(FLAG[i] ^ key[i % len(key)] for i in range(len(FLAG)))
    
    output = {
        "q": q,
        "A": to_int_matrix(A),
        "b": [int(x) for x in b],
        "Bs": to_int_matrix(Bs),
        "enc_flag_hex": enc.hex(),
    }

    with open("output.txt", "w") as f:
        json.dump(output, f)

if __name__ == "__main__":
    main()
