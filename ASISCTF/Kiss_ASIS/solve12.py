#!/usr/bin/env python3
"""
Kiss ASIS - Try different approach

Key insight:
e = inverse(phi + (-1)^r * d, phi)
=> e * (phi + (-1)^r * d) = 1 (mod phi)
=> e * (-1)^r * d = 1 (mod phi)

If r = 0: e * d = 1 (mod phi)  -- standard RSA
If r = 1: e * d = -1 (mod phi) -- means e * d = phi - 1 (mod phi)

Both cases: e * d = t * phi + eps where eps in {1, -1}

For Wiener's attack to work, we need d to be small relative to N^(1/4).
Here d ~ N, so Wiener doesn't work directly.

But there's a generalization: Boneh-Durfee attack works for d < N^0.292.
Here d ~ N, so even that doesn't work.

However, we have additional structure:
- phi = (p^k - 1)(q^k - 1) for k in [1,6]
- This has special algebraic form

Let me try using the fact that for k=1:
phi_1 = (p-1)(q-1) = N - p - q + 1

For k=2:
phi_2 = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)

These factor in special ways. Maybe there's a GCD attack?

Actually, let me think about this differently.
We have e*d = eps (mod phi_k) for some k in [1,6] and eps in {1,-1}.

This means: gcd(e*d - eps, phi_k) >= phi_k for the correct k and eps.
And gcd(e*d - eps, N^k - ...) might reveal something.

Wait, we don't know d! So this doesn't help directly.

New idea: Coppersmith for finding small d.
The equation is: e * d = t * phi_k + eps
Rearranging: e * d - eps = t * phi_k

For k=1: e * d - eps = t * (N - p - q + 1) = t*N - t*(p+q) + t
        e * d - eps = t*N - t*S + t where S = p + q

We have 4 unknowns: d, t, p (or S), and we know:
- p * q = N
- d ~ N
- S ~ 2*sqrt(N)
- t ~ e * d / phi ~ e

This is still complex...

Actually, let me re-read: D = uniform(0.9990, 0.9999)
dbit = int(nbit * D) + 1 = int(1024 * D) + 1

For D in [0.999, 0.9999]:
dbit in [int(1022.976) + 1, int(1023.8976) + 1] = [1023, 1024]

So d has exactly 1023 or 1024 bits. This is almost as big as N (1024 bits).

Hmm, for such large d, the standard attacks don't work.

Let me try a completely different angle: Maybe the sample data I have is
already factored somewhere, or maybe the server generates weak parameters
sometimes.

Let me connect to the server and get fresh parameters, then analyze them.
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd, log2
import sys

def analyze_and_solve(N, e, enc):
    """Try to solve given parameters"""
    
    print(f"\n{'='*60}")
    print(f"Analyzing new parameters:")
    print(f"N bits: {N.bit_length()}")
    print(f"e bits: {e.bit_length()}")
    print(f"{'='*60}")
    
    # Check ratios to guess k
    ratios = {}
    for k in range(1, 7):
        Nk = N ** k
        if e > Nk:
            r = e / Nk
            if r < 10:  # Only meaningful if ratio is small
                ratios[k] = r
                print(f"e / N^{k} = {r:.6f}")
    
    # The right k should have e/N^k close to t/d where t ~ 1 and d ~ N
    # So e/N^k ~ 1/N ... that's tiny
    # Actually for e ~ 0.8 * N^2 (k=2), e/N^2 ~ 0.8 and with d ~ N, t ~ 0.8*N
    
    # Check GCD patterns
    gcd_patterns = {
        'N+1': gcd(e, N+1),
        '(N+1)^2': gcd(e, (N+1)**2),
        'N-1': gcd(e, N-1),
        'N^2-1': gcd(e, N**2 - 1),
    }
    print("\nGCD patterns:")
    for name, g in gcd_patterns.items():
        if g > 1:
            print(f"  gcd(e, {name}) = {g}")
    
    # Try Fermat factorization (quick check)
    print("\nQuick Fermat check...")
    a = isqrt(N) + 1
    for i in range(100000):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            p = a - b
            q = a + b
            if p * q == N:
                print(f"Fermat found factors!")
                return decrypt_with_factors(p, q, N, e, enc)
        a += 1
    
    # Try Pollard rho
    print("\nQuick Pollard rho check...")
    x, y, d = 2, 2, 1
    f = lambda x: (x*x + 1) % N
    for i in range(100000):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x-y), N)
        if d != 1 and d != N:
            print(f"Pollard rho found factor: {d}")
            p = d
            q = N // d
            return decrypt_with_factors(p, q, N, e, enc)
    
    # Try Pollard p-1
    print("\nQuick Pollard p-1 check...")
    a = 2
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        for _ in range(20):
            a = pow(a, p, N)
    g = gcd(a - 1, N)
    if 1 < g < N:
        print(f"Pollard p-1 found factor: {g}")
        p = g
        q = N // g
        return decrypt_with_factors(p, q, N, e, enc)
    
    print("Quick factorization attempts failed.")
    return None

def decrypt_with_factors(p, q, N, e, enc):
    """Try to decrypt with given factors"""
    print(f"\np = {p}")
    print(f"q = {q}")
    
    for k in range(1, 7):
        try:
            phi = (p**k - 1) * (q**k - 1)
            d = pow(e, -1, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            if all(32 <= c <= 126 for c in msg):
                print(f"k={k}: Decrypted message: {msg.decode()}")
                return msg.decode()
        except Exception as ex:
            pass
    
    print("Could not decrypt with any k value")
    return None

def main():
    # First test with sample data
    print("Testing with sample data...")
    
    N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
    e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
    enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842
    
    result = analyze_and_solve(N, e, enc)
    
    if not result:
        print("\n" + "="*60)
        print("Sample data not solved. Trying server...")
        print("="*60)
        
        try:
            io = remote("65.109.214.93", 13137, timeout=20)
            
            # Get parameters
            io.recvuntil(b"[Q]uit")
            io.sendline(b"p")
            
            data = io.recvuntil(b"[Q]uit").decode()
            
            # Parse N
            n_match = data.split("N = ")[1].split("\n")[0].strip()
            N = int(n_match)
            
            # Parse e
            e_match = data.split("e = ")[1].split("\n")[0].strip()
            e = int(e_match)
            
            # Get encrypted message
            io.sendline(b"e")
            data = io.recvuntil(b"[Q]uit").decode()
            enc_match = data.split("enc = ")[1].split("\n")[0].strip()
            enc = int(enc_match)
            
            result = analyze_and_solve(N, e, enc)
            
            if result:
                io.sendline(b"s")
                io.recvuntil(b"secret message:")
                io.sendline(result.encode())
                print(io.recvall(timeout=5).decode())
            
            io.close()
        except Exception as ex:
            print(f"Server error: {ex}")

if __name__ == "__main__":
    main()
