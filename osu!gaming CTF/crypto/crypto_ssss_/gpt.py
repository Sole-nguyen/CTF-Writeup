#!/usr/bin/env python3
import socket, sys, math, itertools, random

HOST = "ssssp.challs.sekai.team"
PORT = 1337

# Field prime from the challenge
P = (1 << 255) - 19

# ---------- small helpers ----------
def egcd(a,b):
    if b==0: return (a,1,0)
    g,x1,y1 = egcd(b, a%b)
    return (g, y1, x1 - (a//b)*y1)

def modinv(a, m):
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("no inverse")
    return x % m

def is_probable_prime(n, k=16):
    if n < 2: return False
    small = [2,3,5,7,11,13,17,19,23,29,31]
    for sp in small:
        if n % sp == 0:
            return n == sp
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2; s += 1
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for __ in range(s - 1):
            x = (x * x) % n
            if x == n - 1: break
        else:
            return False
    return True

def tonelli_shanks(n, p):
    if n == 0: return 0
    if pow(n, (p-1)//2, p) != 1: raise ValueError("nonsquare")
    if p % 4 == 3: return pow(n, (p+1)//4, p)
    q = p - 1; s = 0
    while q % 2 == 0:
        q //= 2; s += 1
    z = 2
    while pow(z, (p-1)//2, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    x = pow(n, (q + 1)//2, p)
    t = pow(n, q, p)
    m = s
    while t != 1:
        i = 1; t2 = (t * t) % p
        while t2 != 1:
            t2 = (t2 * t2) % p; i += 1
        b = pow(c, 1 << (m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    return x

# ----------- poly ops over F_p ------------
def poly_mul(a, b, mod):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0: continue
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % mod
    while out and out[-1] == 0: out.pop()
    return out or [0]

def poly_add(a, b, mod):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(len(a)): out[i] = (out[i] + a[i]) % mod
    for i in range(len(b)): out[i] = (out[i] + b[i]) % mod
    while out and out[-1] == 0: out.pop()
    return out or [0]

def poly_from_points(xs, ys, mod):
    n = len(xs)
    res = [0]
    for i in range(n):
        num = [1]; den = 1; xi = xs[i]
        for j in range(n):
            if j == i: continue
            num = poly_mul(num, [(-xs[j]) % mod, 1], mod)  # (x - xj)
            den = (den * ((xi - xs[j]) % mod)) % mod
        coef = ys[i] * modinv(den, mod) % mod
        term = [(coef * c) % mod for c in num]
        res = poly_add(res, term, mod)
    if len(res) < n: res += [0] * (n - len(res))
    return res  # res[k] is coeff of x^k

# ----------- networking helpers ------------
def recv_until(sock, token: bytes, limit=(1<<20)):
    data = b""
    while token not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > limit:
            break
    return data

def main():
    # Connect and set a read timeout so we never hang forever
    s = socket.create_connection((HOST, PORT))
    s.settimeout(15.0)

    # 1) (Optional) slurp the banner
    _ = recv_until(s, b"welcome")

    # 2) Send all 14 queries at once: ±1..±7  (we send (P - t) for -t mod p)
    ts = [1,2,3,4,5,6,7]
    lines = []
    for t in ts:
        lines.append(str(t))
        lines.append(str((P - t) % P))
    payload = ("\n".join(lines) + "\n").encode()
    s.sendall(payload)

    # 3) Read everything up to the 'secret? ' prompt in one shot
    buf = recv_until(s, b"secret? ")

    # 4) Parse the 14 output lines (lines that are all digits)
    text = buf.decode(errors="ignore")
    digit_lines = [ln.strip() for ln in text.splitlines() if ln.strip().isdigit()]
    ys = [int(ln) for ln in digit_lines[-14:]]  # take the last 14 digit-only lines

    if len(ys) != 14:
        # Dump what we saw to help diagnose
        raise RuntimeError(f"Expected 14 outputs, got {len(ys)}.\n--- got ---\n{text}")

    # Order is y(1), y(p-1), y(2), y(p-2), ..., y(7), y(p-7)
    y_plus  = [ys[2*i]   % P for i in range(7)]
    y_minus = [ys[2*i+1] % P for i in range(7)]

    # 5) Split even/odd and interpolate the odd part
    inv2 = modinv(2, P)
    zs = [(t*t) % P for t in ts]
    Ovals = [ ((yp - ym) * modinv((2*t) % P, P)) % P for t, yp, ym in zip(ts, y_plus, y_minus) ]
    odd_poly = poly_from_points(zs, Ovals, P)  # length 7: c1,c3,...,c13 (mod P)
    odd_mod = [int(x) for x in odd_poly]       # reduce to Python ints

    # 6) Recover the hidden modulus pp from the odd-index subsequence via gcd trick
    best_pp = None
    lifted = None
    for adds in itertools.product((0,1,2), repeat=7):  # lift modulo-p residues to integers
        vec = [ odd_mod[j] + adds[j]*P for j in range(7) ]  # d_j = c_{2j+1}
        deltas = [vec[i+1] - vec[i] for i in range(6)]
        Ts = []
        for j in range(1,5):
            Ts.append(deltas[j+1]*deltas[j-1] - deltas[j]*deltas[j])
        g = 0
        for t in Ts:
            g = math.gcd(g, abs(t))
        if g <= 1: continue
        while g % 2 == 0:
            g //= 2
        if g.bit_length() >= 240 and is_probable_prime(g):
            best_pp = g
            lifted = vec
            break

    if best_pp is None:
        raise RuntimeError("Failed to recover pp. Just run again (different lift) or change ts.")

    pp = best_pp
    d = lifted  # d_j = [c1,c3,...,c13] as integers in [0,pp)

    # 7) Recover LCG params for the odd-subsequence: d_{j+1} = A d_j + B (mod pp)
    A = B = None
    for j in range(5):
        num = (d[j+2] - d[j+1]) % pp
        den = (d[j+1] - d[j]) % pp
        if den % pp == 0: continue
        A = (num * modinv(den, pp)) % pp
        B = (d[j+1] - A*d[j]) % pp
        break
    if A is None:
        raise RuntimeError("Could not compute A,B")

    # 8) a = ±sqrt(A) (mod pp), then b, then SECRET = c0 from c1 = a c0 + b
    root = tonelli_shanks(A, pp)
    candidates = [root, (-root) % pp]
    secret = None

    for a in candidates:
        if (a + 1) % pp == 0:  # degenerate, skip
            continue
        b = (B * modinv((a + 1) % pp, pp)) % pp
        c1 = d[0] % pp
        c0 = (modinv(a, pp) * ((c1 - b) % pp)) % pp  # SECRET
        # Quick verification against a couple outputs
        coeffs = [c0]
        for _ in range(14):
            coeffs.append((a*coeffs[-1] + b) % pp)
        def eval_f(x):
            acc = 0
            powx = 1
            for i, ci in enumerate(coeffs):
                if i == 0:
                    term = ci % P
                else:
                    powx = (powx * x) % P
                    term = (ci % P) * powx % P
                acc = (acc + term) % P
            return acc
        ok = True
        for t, yp, ym in zip(ts, y_plus, y_minus):
            if eval_f(t) != yp or eval_f((P - t) % P) != ym:
                ok = False; break
        if ok:
            secret = int(c0)
            break

    if secret is None:
        raise RuntimeError("Square-root/lift mismatch; rerun (rare)")

    # 9) Send the secret and print the flag
    s.sendall(str(secret).encode() + b"\n")
    # Read one line (the flag)
    flag = recv_until(s, b"\n").decode(errors="ignore").strip()
    print(flag)

if __name__ == "__main__":
    main()
