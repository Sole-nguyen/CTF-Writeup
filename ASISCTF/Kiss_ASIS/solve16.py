#!/usr/bin/env python3
"""
Kiss ASIS - Direct solver
Try brute force with small t values across all k in {1,2,3,4,5,6}

Key equations:
- e*d = t * phi_k + r  where r = +/-1
- phi_k = (p^k - 1)(q^k - 1)

For each k, we can express phi_k in terms of N and s = p+q
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import time

context.log_level = 'error'

def solve_quadratic(s, N):
    """Given s = p+q and N = p*q, find p, q"""
    disc = s*s - 4*N
    if disc < 0:
        return None, None
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None, None
    p = (s + sqrt_disc) // 2
    q = (s - sqrt_disc) // 2
    if p * q == N and p > 1 and q > 1:
        return p, q
    return None, None

def compute_phi(p, q, k):
    """Compute phi_k = (p^k - 1)(q^k - 1)"""
    return (p**k - 1) * (q**k - 1)

def try_solve(N, e, enc, max_t=1000):
    """Try to solve given N, e, enc"""
    
    print(f"  N bits: {N.bit_length()}, e bits: {e.bit_length()}")
    
    # For each possible k, try small t values
    for k in [1, 2, 3, 4, 5, 6]:
        print(f"    Trying k={k}...", end=" ", flush=True)
        
        found = False
        for t in range(1, max_t):
            for r in [1, -1]:
                # e*d = t*phi + r
                # For various phi approximations, estimate d
                
                if k == 1:
                    # phi ~ N - sqrt(N)*2 ~ N
                    phi_approx = N
                elif k == 2:
                    # phi ~ N^2
                    phi_approx = N * N
                else:
                    # phi ~ N^k
                    phi_approx = N ** k
                
                # d ~ (t * phi + r) / e
                d_approx = (t * phi_approx) // e
                
                if d_approx <= 0:
                    continue
                
                # Try nearby d values
                for d_delta in range(-5, 6):
                    d = d_approx + d_delta
                    if d <= 1:
                        continue
                    
                    val = e * d - r
                    if val <= 0 or val % t != 0:
                        continue
                    
                    phi = val // t
                    
                    # Now try to verify this phi
                    # For k=1: phi = (p-1)(q-1) = N + 1 - s
                    # For k=2: phi = (N+1)^2 - s^2
                    # etc.
                    
                    if k == 1:
                        s = N + 1 - phi
                        if s > 0:
                            p, q = solve_quadratic(s, N)
                            if p is not None:
                                real_phi = compute_phi(p, q, k)
                                if real_phi == phi:
                                    print(f"FOUND! t={t}, d={d}")
                                    return p, q, k, d
                    elif k == 2:
                        s_sq = (N+1)**2 - phi
                        if s_sq > 0:
                            s = isqrt(s_sq)
                            if s*s == s_sq:
                                p, q = solve_quadratic(s, N)
                                if p is not None:
                                    real_phi = compute_phi(p, q, k)
                                    if real_phi == phi:
                                        print(f"FOUND! t={t}, d={d}")
                                        return p, q, k, d
        print("not found")
    
    return None, None, None, None

def try_server(max_t=200):
    """Try to solve one server instance"""
    try:
        io = remote("65.109.214.93", 13137, timeout=20)
        io.recvuntil(b"[Q]uit", timeout=10)
        io.sendline(b"p")
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        
        N, e = None, None
        for line in data.split("\n"):
            if "N = " in line: N = int(line.split("N = ")[1].strip())
            if "e = " in line: e = int(line.split("e = ")[1].strip())
        
        if N is None or e is None:
            io.close()
            return False, None
        
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        
        enc = None
        for line in data.split("\n"):
            if "enc = " in line: enc = int(line.split("enc = ")[1].strip())
        
        if enc is None:
            io.close()
            return False, None
        
        p, q, k, d = try_solve(N, e, enc, max_t)
        
        if p is not None:
            # Decrypt
            phi = compute_phi(p, q, k)
            d = pow(e, -1, phi)
            m = pow(enc, d, N)
            msg = long_to_bytes(m)
            
            try:
                msg_str = msg.decode()
                if all(32 <= ord(c) <= 126 for c in msg_str):
                    print(f"  Decrypted: {msg_str}")
                    
                    # Submit
                    io.sendline(b"s")
                    io.recvuntil(b"secret message:", timeout=5)
                    io.sendline(msg_str.encode())
                    response = io.recvall(timeout=5).decode()
                    print(f"  Response: {response}")
                    io.close()
                    return True, response
            except:
                pass
        
        io.close()
        return False, None
    
    except Exception as ex:
        print(f"  Error: {ex}")
        return False, None

def main():
    print("="*60)
    print("Kiss ASIS - Direct Solver with Small t")
    print("="*60)
    
    for attempt in range(50):
        print(f"\nAttempt {attempt+1}...")
        
        success, response = try_server(max_t=500)
        
        if success:
            print("\nSUCCESS!")
            print(response)
            break
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
