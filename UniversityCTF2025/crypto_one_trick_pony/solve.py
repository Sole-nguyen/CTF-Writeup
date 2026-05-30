import hashlib
import json
import socket
from math import isqrt
import time

# ===== Constants from the challenge =====
FROST_PRIME = int(
    "1a66804d885939d7acf3a4b413c9a24547b876e706913adec9684cc4a63ab0df"
    "d2e0fd79f683de06ad17774815dfc8375370eb3d0fb5dce0019bd0632e7663a41",
    16,
)
ORDER = FROST_PRIME - 1

# Factorization of ORDER (computed once offline):
# {2: 6, 3: 35, 5: 21, 7: 6, 137: 11, 191: 2, 331: 3, 3469: 2, 3613: 11, 3967: 6, 16561: 3}
ORDER_FACTORS = [
    (2, 6),
    (3, 35),
    (5, 21),
    (7, 6),
    (137, 11),
    (191, 2),
    (331, 3),
    (3469, 2),
    (3613, 11),
    (3967, 6),
    (16561, 3),
]


def sha512_int(msg: str) -> int:
    return int.from_bytes(hashlib.sha512(msg.encode()).digest(), "big") % FROST_PRIME


def is_generator(g: int) -> bool:
    if g % FROST_PRIME == 0:
        return False
    for q, _e in ORDER_FACTORS:
        if pow(g, ORDER // q, FROST_PRIME) == 1:
            return False
    return True


def crt_pair(a1: int, n1: int, a2: int, n2: int) -> tuple[int, int]:
    """Return (a, n) solving x=a mod n for the two congruences; n1,n2 coprime."""
    # a = a1 + n1 * t
    t = ((a2 - a1) % n2) * pow(n1, -1, n2) % n2
    a = a1 + n1 * t
    return a % (n1 * n2), n1 * n2


class PohligHellman:
    def __init__(self, g: int):
        if not is_generator(g):
            raise ValueError("base is not a generator; pick another message")
        self.g = g % FROST_PRIME
        # For each prime q, base_q = g^(ORDER/q) has order q.
        self._prime_base = {}
        self._prime_logtbl = {}
        for q, _e in ORDER_FACTORS:
            base_q = pow(self.g, ORDER // q, FROST_PRIME)
            self._prime_base[q] = base_q
            tbl = {}
            cur = 1
            # q is at most 16561, so this is cheap.
            for j in range(q):
                tbl[cur] = j
                cur = (cur * base_q) % FROST_PRIME
            self._prime_logtbl[q] = tbl

    def dlog(self, h: int) -> int:
        """Solve g^x = h (mod FROST_PRIME) for x in [0, ORDER)."""
        h %= FROST_PRIME
        if h == 0:
            raise ValueError("h=0 is not in multiplicative group")

        residues = []
        for q, e in ORDER_FACTORS:
            qpow = q**e
            m = ORDER // qpow
            g0 = pow(self.g, m, FROST_PRIME)
            h0 = pow(h, m, FROST_PRIME)

            x_qe = 0
            # base in the order-q subgroup (constant for this q)
            base_q = self._prime_base[q]
            logtbl = self._prime_logtbl[q]

            for k in range(e):
                # c = (h0 * g0^{-x_qe})^{q^{e-1-k}}  in subgroup of order q
                gx = pow(g0, x_qe, FROST_PRIME)
                inv_gx = pow(gx, FROST_PRIME - 2, FROST_PRIME)
                c = pow((h0 * inv_gx) % FROST_PRIME, q ** (e - 1 - k), FROST_PRIME)
                d = logtbl.get(c)
                if d is None:
                    raise ValueError("unexpected: discrete log lookup failed")
                x_qe += d * (q**k)

            residues.append((x_qe, qpow))

        x, mod = 0, 1
        for a_i, n_i in residues:
            x, mod = crt_pair(x, mod, a_i, n_i)
        return x % mod


def legendre_bit(a: int, p: int) -> int:
    # Euler criterion for prime p: a^((p-1)/2) mod p is 1 or p-1 (or 0 if a==0).
    return 1 if pow(a % p, (p - 1) // 2, p) == 1 else 0


class Remote:
    def __init__(self, host: str, port: int):
        self.s = socket.create_connection((host, port))
        self.buf = b""

    def close(self):
        try:
            self.s.close()
        except Exception:
            pass

    def _recv_some(self):
        data = self.s.recv(65536)
        if not data:
            raise EOFError("connection closed")
        self.buf += data

    def recv_until(self, token: bytes) -> bytes:
        while token not in self.buf:
            self._recv_some()
        out, self.buf = self.buf.split(token, 1)
        return out + token

    def recv_line(self) -> bytes:
        return self.recv_until(b"\n")

    def send_line(self, line: str):
        self.s.sendall(line.encode() + b"\n")


def find_shift_index(obs_bits: list[int], p: int, *, L: int = 64, J_mult: int = 6, verify: int = 4096) -> int:
    """Recover idx0 in Z_(p-1) such that obs_bits[i] = legendre_bit(idx0+i+1 mod (p-1), p)."""
    m = p - 1
    B = isqrt(m) + 1

    if len(obs_bits) < L + verify:
        raise ValueError("need more observed bits to recover shift")

    J = min(len(obs_bits) - L, J_mult * B)
    if J <= 0:
        raise ValueError("not enough bits for window table")

    mask = (1 << L) - 1

    # Rolling window signature over observed bits.
    sig = 0
    for i in range(L):
        sig = ((sig << 1) | obs_bits[i]) & mask

    table: dict[int, list[int]] = {sig: [0]}
    for j in range(1, J):
        sig = ((sig << 1) | obs_bits[j + L - 1]) & mask
        table.setdefault(sig, []).append(j)

    def cand_sig(idx: int) -> int:
        s = 0
        for r in range(L):
            a = ((idx + r) % m) + 1
            s = (s << 1) | legendre_bit(a, p)
        return s

    def verify_idx(idx0: int) -> bool:
        for i in range(verify):
            a = ((idx0 + i) % m) + 1
            if legendre_bit(a, p) != obs_bits[i]:
                return False
        return True

    for k in range(B):
        idx = (k * B) % m
        s = cand_sig(idx)
        js = table.get(s)
        if not js:
            continue
        for j in js:
            idx0 = (idx - j) % m
            if verify_idx(idx0):
                return idx0

    raise RuntimeError("failed to recover shift; try collecting more signatures or adjusting parameters")


def main():
    host = "154.57.164.77"
    port = 32759

    # Tunables: trade off requests vs. robustness.
    L = 64
    J_mult = 4
    verify = 2048

    # 1) Find a message whose snowmark is a generator of (Z/pZ)^*
    msg = None
    for i in range(1, 20000):
        cand = f"msg-{i}"
        g = sha512_int(cand)
        if is_generator(g):
            msg = cand
            break
    if msg is None:
        raise RuntimeError("could not find generator message (unexpected)")

    g = sha512_int(msg)
    ph = PohligHellman(g)

    # 2) Connect and parse holly_prime
    r = Remote(host, port)
    try:
        # read until holly_prime line is present
        banner = r.recv_until(b"\n")
        holly_prime = None
        # consume lines until we see it
        while holly_prime is None:
            line = banner.decode(errors="ignore")
            if "frostrng.holly_prime" in line and "=" in line:
                holly_prime = int(line.split("=")[-1].strip())
                break
            banner = r.recv_until(b"\n")

        p = holly_prime
        m = p - 1

        # 3) Collect signatures and recover RNG bits
        # Need roughly ~J_mult*sqrt(p) windows; each signature yields 500 bits.
        B = isqrt(m) + 1
        target_bits = J_mult * B + L + verify
        N = (target_bits + 499) // 500
        if N > 1900:
            N = 1900

        obs_bits: list[int] = []

        t0 = time.time()
        for i in range(N):
            r.recv_until(b"> ")
            r.send_line("1")
            r.recv_until(b"Whisper your message: ")
            r.send_line(msg)
            line = r.recv_line()
            try:
                sig_val = int(json.loads(line.decode())['signature'])
            except Exception:
                # sometimes prompts may be interleaved; keep reading until JSON
                while True:
                    if b"{" in line and b"signature" in line:
                        sig_val = int(json.loads(line.decode())['signature'])
                        break
                    line = r.recv_line()

            k = ph.dlog(sig_val)
            bits = format(k, "b").zfill(500)
            obs_bits.extend(1 if ch == "1" else 0 for ch in bits)

            if (i + 1) % 25 == 0:
                dt = time.time() - t0
                print(f"[+] collected {i+1}/{N} signatures ({len(obs_bits)} bits) in {dt:.1f}s", flush=True)

        # 4) Recover initial shift (idx0) and predict OTP bits at current state
        idx0 = find_shift_index(obs_bits, p, L=L, J_mult=J_mult, verify=verify)

        steps = 500 * N
        idx_cur = (idx0 + steps) % m

        # Flag length is 4 + 79 + 1 = 84 => 672 bits.
        otp_len = 84 * 8
        otp_bits = []
        for i in range(otp_len):
            a = ((idx_cur + i) % m) + 1
            otp_bits.append("1" if legendre_bit(a, p) == 1 else "0")
        otp_str = "".join(otp_bits)

        # 5) Request flag
        r.recv_until(b"> ")
        r.send_line("2")
        r.recv_until(b"Reveal my snow-otp (in bits): ")
        r.send_line(otp_str)
        resp = r.recv_line().decode(errors="ignore")
        print(resp)

    finally:
        r.close()


if __name__ == "__main__":
    main()
