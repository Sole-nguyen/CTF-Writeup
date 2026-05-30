#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import socket
from typing import List

try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES


class LineReader:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buffer = b""

    def readline(self) -> str:
        while b"\n" not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed")
            self.buffer += chunk
        line, self.buffer = self.buffer.split(b"\n", 1)
        return line.decode(errors="replace").strip()


def mul(a: List[int], b: List[int], poly: List[int]) -> List[int]:
    deg = 8
    prod = [0] * (2 * deg - 1)
    for i in range(deg):
        ai = a[i]
        for j in range(deg):
            prod[i + j] = (prod[i + j] + ai * b[j]) % 4

    for d in range(2 * deg - 2, deg - 1, -1):
        coeff = prod[d]
        if coeff:
            for k in range(deg + 1):
                prod[d - deg + k] = (prod[d - deg + k] - coeff * poly[k]) % 4
            prod[d] = 0
    return prod[:deg]


def kdf(secret_key: List[int], poly_coeffs: List[int], gen_coeffs: List[int]) -> bytes:
    sk_bytes = bytes([e + 127 for e in secret_key])
    h = hashlib.shake_256(sk_bytes)
    state_bytes = h.digest(136)

    mixed = bytearray()
    for off in range(0, len(state_bytes), 8):
        block = state_bytes[off:off + 8]
        if len(block) < 8:
            block = block + bytes(8 - len(block))
        elem = [int(b) % 4 for b in block]
        product = mul(elem, gen_coeffs, poly_coeffs)
        mixed.extend(bytes(c % 256 for c in product))

    squeeze = h.digest(32)
    derived = hashlib.shake_256(bytes(mixed)).digest(32)
    return bytes(a ^ b for a, b in zip(derived, squeeze))


def solve_vandermonde(xs: List[int], ys: List[int], p: int) -> List[int]:
    n = len(xs)
    mat = [[0] * (n + 1) for _ in range(n)]

    for i, x in enumerate(xs):
        val = 1
        for j in range(n):
            mat[i][j] = val
            val = (val * x) % p
        mat[i][n] = ys[i] % p

    for col in range(n):
        pivot = None
        for r in range(col, n):
            if mat[r][col] % p != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Singular matrix")
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]

        inv = pow(mat[col][col], -1, p)
        for c in range(col, n + 1):
            mat[col][c] = (mat[col][c] * inv) % p

        for r in range(n):
            if r == col:
                continue
            factor = mat[r][col]
            if factor == 0:
                continue
            for c in range(col, n + 1):
                mat[r][c] = (mat[r][c] - factor * mat[col][c]) % p

    return [mat[i][n] for i in range(n)]


def recv_params(reader: LineReader):
    params = None
    flag_ct = flag_nonce = flag_tag = None
    while True:
        line = reader.readline()
        if line.startswith("PARAMS "):
            raw = base64.b64decode(line.split(" ", 1)[1])
            params = json.loads(raw)
        elif line.startswith("ENCRYPTED_FLAG "):
            parts = line.split()
            flag_ct = bytes.fromhex(parts[1])
            flag_nonce = bytes.fromhex(parts[2])
            flag_tag = bytes.fromhex(parts[3])
        elif line == "READY":
            break
    if params is None or flag_ct is None:
        raise RuntimeError("Missing parameters from server")
    return params, flag_ct, flag_nonce, flag_tag


def recover_flag(host: str, port: int, timeout: float):
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        reader = LineReader(sock)
        params, flag_ct, flag_nonce, flag_tag = recv_params(reader)

        p = int(params["p"])
        primes = [int(x) for x in params["primes"]]
        gr48_poly = [int(x) for x in params["gr48_poly"]]
        gr48_gen = [int(x) for x in params["gr48_generator"]]

        n = len(primes)
        xs = []
        x = 0
        while len(xs) < n:
            if (x * x) % p == 4 % p:
                x += 1
                continue
            xs.append(x)
            x += 1

        ys = []
        ops_count = None
        for A in xs:
            sock.sendall(f"QUERY {A}\n".encode())
            line = reader.readline()
            parts = line.split()
            if not parts or parts[0] != "RESULT":
                raise RuntimeError(f"Unexpected response: {line}")
            if ops_count is None:
                ops_count = int(parts[2])
            ys.append(int(parts[3]))

    coeffs = solve_vandermonde(xs, ys, p)
    signed = [c if c <= p // 2 else c - p for c in coeffs]

    zero_indices = [i for i, v in enumerate(signed) if v == 0]
    sum_abs = sum(abs(v) for v in signed)
    abs_missing = ops_count - sum_abs
    if abs_missing < 0:
        raise RuntimeError("Inconsistent ops_count vs recovered coefficients")

    candidates = []
    if abs_missing == 0:
        candidates = [signed]
    else:
        for idx in zero_indices:
            for sign in (1, -1):
                candidate = signed.copy()
                candidate[idx] = sign * abs_missing
                if all(-127 <= v <= 128 for v in candidate):
                    candidates.append(candidate)

    for candidate in candidates:
        key = kdf(candidate, gr48_poly, gr48_gen)
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=flag_nonce)
            flag = cipher.decrypt_and_verify(flag_ct, flag_tag)
            return flag.decode()
        except ValueError:
            continue

    raise RuntimeError("No candidate key verified the flag")


def main():
    parser = argparse.ArgumentParser(description="Portobelo solver")
    parser.add_argument("--host", default="portobelo.ctf.ritsec.club")
    parser.add_argument("--port", type=int, default=1337)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    flag = recover_flag(args.host, args.port, args.timeout)
    print(flag)


if __name__ == "__main__":
    main()
