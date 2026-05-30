import argparse
import hashlib
import json
import socket
import sys
from dataclasses import dataclass
from typing import List, Tuple


HEX_BYTES = [
    *list(range(ord('0'), ord('9') + 1)),
    *list(range(ord('a'), ord('f') + 1)),
]


# AES S-box
SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]


def pad_pkcs7(m: bytes, bs: int = 16) -> bytes:
    n = bs - (len(m) % bs)
    return m + bytes([n]) * n


def b2m(block16: bytes) -> List[List[int]]:
    assert len(block16) == 16
    return [
        [block16[4 * c + r] for r in range(4)]
        for c in range(4)
    ]


def m2b(state: List[List[int]]) -> bytes:
    out = bytearray(16)
    for c in range(4):
        for r in range(4):
            out[4 * c + r] = state[c][r] & 0xFF
    return bytes(out)


def sr(state):
    # same as server.py
    res = [state[i].copy() for i in range(4)]
    res[0][1], res[1][1], res[2][1], res[3][1] = res[1][1], res[2][1], res[3][1], res[0][1]
    res[0][2], res[1][2], res[2][2], res[3][2] = res[2][2], res[3][2], res[0][2], res[1][2]
    res[0][3], res[1][3], res[2][3], res[3][3] = res[3][3], res[0][3], res[1][3], res[2][3]
    return res


def xtime(x: int) -> int:
    x &= 0xFF
    return (((x << 1) & 0xFF) ^ (0x1B if (x & 0x80) else 0)) & 0xFF


def mc_col(col: List[int]) -> List[int]:
    a0, a1, a2, a3 = [x & 0xFF for x in col]
    m2 = [xtime(x) for x in (a0, a1, a2, a3)]
    m3 = [(m2[i] ^ (a0, a1, a2, a3)[i]) & 0xFF for i in range(4)]
    b0 = (m2[0] ^ m3[1] ^ a2 ^ a3) & 0xFF
    b1 = (a0 ^ m2[1] ^ m3[2] ^ a3) & 0xFF
    b2 = (a0 ^ a1 ^ m2[2] ^ m3[3]) & 0xFF
    b3 = (m3[0] ^ a1 ^ a2 ^ m2[3]) & 0xFF
    return [b0, b1, b2, b3]


def encrypt_block_1r(block16: bytes, k0: bytes, k1: bytes) -> bytes:
    s = b2m(block16)
    rk0 = b2m(k0)
    rk1 = b2m(k1)
    # add round key
    for c in range(4):
        for r in range(4):
            s[c][r] ^= rk0[c][r]
    # sub bytes
    for c in range(4):
        for r in range(4):
            s[c][r] = SBOX[s[c][r]]
    s = sr(s)
    s = [mc_col(s[c]) for c in range(4)]
    for c in range(4):
        for r in range(4):
            s[c][r] ^= rk1[c][r]
    return m2b(s)


@dataclass
class Sample:
    uid: int
    token: bytes


class SockReader:
    """Small buffered reader so recv_until doesn't over-read past delimiters."""

    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf = bytearray()

    def recv_until(self, marker: bytes, limit: int = 1 << 20) -> bytes:
        while True:
            idx = self.buf.find(marker)
            if idx != -1:
                end = idx + len(marker)
                out = bytes(self.buf[:end])
                del self.buf[:end]
                return out

            chunk = self.sock.recv(4096)
            if not chunk:
                raise EOFError("connection closed")
            self.buf += chunk
            if len(self.buf) > limit:
                raise RuntimeError("recv_until overflow")


def recv_until(sock: socket.socket, marker: bytes, limit: int = 1 << 20) -> bytes:
    # Backwards-compatible helper when buffering doesn't matter.
    r = SockReader(sock)
    return r.recv_until(marker, limit=limit)


def get_samples(host: str, port: int, count: int, username: str) -> List[Sample]:
    samples: List[Sample] = []
    with socket.create_connection((host, port), timeout=10) as s:
        s.settimeout(10)
        r = SockReader(s)
        for _ in range(count):
            r.recv_until(b"> ")
            s.sendall(b"1\n")
            r.recv_until(b"Enter username: ")
            s.sendall(username.encode() + b"\n")
            # read lines until we find the JSON response
            while True:
                line = r.recv_until(b"\n")
                if b"{\"token\":" in line or line.lstrip().startswith(b"{"):
                    obj = json.loads(line.decode().strip())
                    break
            token = bytes.fromhex(obj["token"])
            # uid starts at 1 and increments
            uid = len(samples) + 1
            samples.append(Sample(uid=uid, token=token))
    return samples


def build_plaintext_template(uid: int) -> Tuple[bytes, List[int]]:
    """Return (padded_plaintext, hex_positions) where hex_positions are byte indices within padded_plaintext that are snowprint hex chars."""
    prefix = b'{"s": "'
    mid = b'", "i": '
    suffix = b"}"
    uid_b = str(uid).encode()

    # 128 bytes of unknown hex chars
    # We'll mark their indices in the final padded plaintext.
    base = prefix + (b"?" * 128) + mid + uid_b + suffix
    hex_positions = list(range(len(prefix), len(prefix) + 128))
    padded = pad_pkcs7(base, 16)
    return padded, hex_positions


def build_tail_plaintext(uid: int) -> Tuple[bytes, List[int]]:
    """Return last 32 bytes of the padded plaintext, plus indices (0..31) that are unknown hex chars.

    This drastically reduces SMT size while still giving strong constraints, because the last two
    blocks contain the fixed JSON trailer and PKCS#7 padding, plus only the final 7 hex chars.
    """
    full, hex_pos = build_plaintext_template(uid)
    tail_start = len(full) - 32
    tail = full[tail_start:]
    tail_hex = [i - tail_start for i in hex_pos if tail_start <= i < tail_start + 32]
    return tail, tail_hex


def solve_keys_z3(samples: List[Sample], verbose: bool = True) -> Tuple[bytes, bytes]:
    try:
        import z3  # type: ignore
    except ImportError as e:
        raise SystemExit(
            "Missing dependency: z3-solver. Install it with: pip install z3-solver"
        ) from e

    def bv8(name: str):
        return z3.BitVec(name, 8)

    def bv8v(x: int):
        return z3.BitVecVal(x & 0xFF, 8)

    # z3 helpers for AES ops
    sbox_bv = [bv8v(x) for x in SBOX]

    def sbox(x):
        return z3.Select(z3.Array('SBOX', z3.BitVecSort(8), z3.BitVecSort(8)), x)  # placeholder

    # Build an actual Array for SBOX
    SBOX_ARR = z3.K(z3.BitVecSort(8), bv8v(0))
    for i, v in enumerate(SBOX):
        SBOX_ARR = z3.Store(SBOX_ARR, bv8v(i), bv8v(v))

    def sb(x):
        return z3.Select(SBOX_ARR, x)

    def xt(x):
        msb = z3.Extract(7, 7, x)  # (_ BitVec 1)
        shifted = z3.Extract(7, 0, x << 1)
        return z3.If(msb == z3.BitVecVal(1, 1), shifted ^ bv8v(0x1B), shifted)

    def mul2(x):
        return xt(x)

    def mul3(x):
        return mul2(x) ^ x

    def mc(col):
        a0, a1, a2, a3 = col
        b0 = mul2(a0) ^ mul3(a1) ^ a2 ^ a3
        b1 = a0 ^ mul2(a1) ^ mul3(a2) ^ a3
        b2 = a0 ^ a1 ^ mul2(a2) ^ mul3(a3)
        b3 = mul3(a0) ^ a1 ^ a2 ^ mul2(a3)
        return [b0, b1, b2, b3]

    def sr_cols(cols):
        # cols: 4 columns, each 4 bytes
        res = [cols[i][:] for i in range(4)]
        # rotate row 1 across columns
        res[0][1], res[1][1], res[2][1], res[3][1] = res[1][1], res[2][1], res[3][1], res[0][1]
        # rotate row 2 across columns by 2
        res[0][2], res[1][2], res[2][2], res[3][2] = res[2][2], res[3][2], res[0][2], res[1][2]
        # rotate row 3 across columns by 3
        res[0][3], res[1][3], res[2][3], res[3][3] = res[3][3], res[0][3], res[1][3], res[2][3]
        return res

    def xor_state(a, b):
        return [[a[c][r] ^ b[c][r] for r in range(4)] for c in range(4)]

    # unknown keys (assume KEY = k0||k1)
    k0 = [bv8(f"k0_{i}") for i in range(16)]
    k1 = [bv8(f"k1_{i}") for i in range(16)]

    # We don't have the challenge's b2m/m2b, so we try two common layouts.
    # - 'col': AES column-major state (outer index = column)
    # - 'row': row-major state (outer index = row)
    def as_state(vec16, layout_: str):
        if layout_ == 'col':
            return [[vec16[4 * c + r] for r in range(4)] for c in range(4)]
        if layout_ == 'row':
            return [[vec16[4 * r + c] for c in range(4)] for r in range(4)]
        raise ValueError(f"unknown layout: {layout_}")

    def flatten_state(st, layout_: str):
        if layout_ == 'col':
            return [st[c][r] for c in range(4) for r in range(4)]
        if layout_ == 'row':
            return [st[r][c] for r in range(4) for c in range(4)]
        raise ValueError(f"unknown layout: {layout_}")

    for layout in ("col", "row"):
        rk0 = as_state(k0, layout)
        rk1 = as_state(k1, layout)

        solver = z3.Solver()
        # Prevent pathological hangs if our cipher assumptions are off.
        solver.set(timeout=60_000)  # milliseconds

        for si, smp in enumerate(samples):
            pt_tail, hex_pos = build_tail_plaintext(smp.uid)
            if len(smp.token) < 32:
                raise ValueError(f"Unexpected token length for uid {smp.uid}: {len(smp.token)}")
            ct_tail = smp.token[-32:]

            # Create plaintext bytes as BitVecs/const
            pbytes = []
            for idx, b in enumerate(pt_tail):
                if idx in hex_pos:
                    v = bv8(f"p{si}_{idx}")
                    # constrain to lowercase hex
                    solver.add(z3.Or([v == bv8v(h) for h in HEX_BYTES]))
                    pbytes.append(v)
                else:
                    pbytes.append(bv8v(b))

            # For each block, enforce encryption relation
            for blk in range(0, 32, 16):
                pblk = pbytes[blk:blk + 16]
                cblk = ct_tail[blk:blk + 16]
                s = as_state(pblk, layout)
                s = xor_state(s, rk0)
                s = [[sb(s[c][r]) for r in range(4)] for c in range(4)]
                s = sr_cols(s)
                s = [mc(s[c]) for c in range(4)]
                s = xor_state(s, rk1)
                out = flatten_state(s, layout)
                for i in range(16):
                    solver.add(out[i] == bv8v(cblk[i]))

        if verbose:
            print(f"[+] Trying layout='{layout}' with {len(samples)} samples ({len(samples)*2} blocks)...", flush=True)

        if solver.check() == z3.sat:
            model = solver.model()
            k0_bytes = bytes([model.evaluate(k0[i]).as_long() for i in range(16)])
            k1_bytes = bytes([model.evaluate(k1[i]).as_long() for i in range(16)])
            if verbose:
                print(f"[+] SAT with layout='{layout}'", flush=True)
                print(f"[+] Recovered k0={k0_bytes.hex()}", flush=True)
                print(f"[+] Recovered k1={k1_bytes.hex()}", flush=True)
            return k0_bytes, k1_bytes

    raise RuntimeError("Z3 reported UNSAT for both layouts (cipher assumptions likely wrong)")


def forge_admin_token(k0: bytes, k1: bytes) -> str:
    key = k0 + k1
    username = b"TinselwickAdmin"
    uid = 0
    snow = hashlib.shake_256(key + username + str(uid).encode()).digest(64).hex().encode()
    msg = b'{"s": "' + snow + b'", "i": 0}'
    msg = pad_pkcs7(msg, 16)
    ct = b"".join(
        encrypt_block_1r(msg[i:i+16], k0, k1)
        for i in range(0, len(msg), 16)
    )
    return ct.hex()


def login(host: str, port: int, uid: int, username: str, token_hex: str) -> str:
    with socket.create_connection((host, port), timeout=10) as s:
        s.settimeout(10)
        r = SockReader(s)
        r.recv_until(b"> ")
        s.sendall(b"2\n")
        r.recv_until(b"Enter UID: ")
        s.sendall(f"{uid}\n".encode())
        r.recv_until(b"Enter username: ")
        s.sendall(username.encode() + b"\n")
        r.recv_until(b"Enter token (hex): ")
        s.sendall(token_hex.encode() + b"\n")
        line = r.recv_until(b"\n")
        return line.decode(errors="replace")


def main():
    ap = argparse.ArgumentParser(description="Solve UniversityCTF2025 crypto_disguised")
    ap.add_argument("--host", default="154.57.164.69")
    ap.add_argument("--port", type=int, default=31239)
    ap.add_argument("--samples", type=int, default=12, help="number of register tokens to collect (max 31 per connection)")
    ap.add_argument("--username", default="nhat", help="username used during registration")
    ap.add_argument("--no-login", action="store_true")
    args = ap.parse_args()

    print(f"[+] Collecting {args.samples} samples from {args.host}:{args.port}...")
    samples = get_samples(args.host, args.port, args.samples, args.username)

    print("[+] Solving for keys with Z3 (this may take a bit)...")
    k0, k1 = solve_keys_z3(samples, verbose=True)

    admin_token = forge_admin_token(k0, k1)
    print(f"[+] Forged admin token: {admin_token}")

    if not args.no_login:
        print("[+] Logging in as admin...")
        resp = login(args.host, args.port, 0, "TinselwickAdmin", admin_token)
        print(resp)


if __name__ == "__main__":
    main()
