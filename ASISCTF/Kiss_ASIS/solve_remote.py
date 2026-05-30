#!/usr/bin/env python3
"""
Kiss ASIS - Connect to server and solve
"""

from pwn import *
from Crypto.Util.number import *
from math import gcd, isqrt
import re

context.log_level = 'info'

def get_convergents(num, den):
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    a, b = num, den
    while b:
        q = a // b
        h_prev, h_curr = h_curr, q * h_curr + h_prev
        k_prev, k_curr = k_curr, q * k_curr + k_prev
        yield (h_curr, k_curr)
        a, b = b, a % b

def factor_from_phi(N, phi, k):
    """Given phi = (p^k - 1)(q^k - 1), find p, q"""
    if k == 1:
        S = N + 1 - phi
        disc = S*S - 4*N
        if disc < 0:
            return None, None
        sqrt_disc = isqrt(disc)
        if sqrt_disc * sqrt_disc != disc:
            return None, None
        p = (S + sqrt_disc) // 2
        q = (S - sqrt_disc) // 2
        if p * q == N:
            return p, q
        return None, None
    
    elif k == 2:
        S_sq = (N+1)**2 - phi
        if S_sq <= 0:
            return None, None
        S = isqrt(S_sq)
        if S*S != S_sq:
            return None, None
        disc = S*S - 4*N
        if disc < 0:
            return None, None
        sqrt_disc = isqrt(disc)
        if sqrt_disc * sqrt_disc != disc:
            return None, None
        p = (S + sqrt_disc) // 2
        q = (S - sqrt_disc) // 2
        if p * q == N:
            return p, q
        return None, None
    
    elif k == 3:
        RHS = N**3 + 1 - phi
        S = 2 * isqrt(N)
        for _ in range(200):
            f = S**3 - 3*N*S - RHS
            fp = 3*S*S - 3*N
            if fp == 0:
                break
            S_new = S - f // fp
            if abs(S_new - S) <= 1:
                break
            S = S_new
        
        for delta in range(-10, 11):
            SS = S + delta
            if SS > 0 and SS**3 - 3*N*SS == RHS:
                disc = SS*SS - 4*N
                if disc < 0:
                    continue
                sqrt_disc = isqrt(disc)
                if sqrt_disc * sqrt_disc != disc:
                    continue
                p = (SS + sqrt_disc) // 2
                q = (SS - sqrt_disc) // 2
                if p * q == N:
                    return p, q
        return None, None
    
    return None, None

def attack(N, e, enc):
    """Try to factor N and decrypt"""
    print(f"[*] N bits: {N.bit_length()}")
    print(f"[*] e bits: {e.bit_length()}")
    
    # Determine likely k based on e size
    # For k: e ≈ phi ≈ N^k, or more precisely e*d ≈ phi where d ≈ N
    # So e ≈ N^(k-1)
    
    e_bits = e.bit_length()
    n_bits = N.bit_length()
    k_estimate = e_bits // n_bits + 1
    print(f"[*] Estimated k based on e/N ratio: {k_estimate}")
    
    # Try each k value
    for k in range(1, 7):
        print(f"\n[*] Trying k = {k}")
        phi_approx = N ** k
        
        # Method 1: Continued fractions on e/phi_approx
        conv_count = 0
        for B, d in get_convergents(e, phi_approx):
            conv_count += 1
            if conv_count > 1000:
                break
            
            # Check d size
            d_bits = d.bit_length()
            if not (n_bits - 10 <= d_bits <= n_bits + 10):
                continue
            
            for sign in [1, -1]:
                if B == 0:
                    continue
                val = e * d + sign
                if val % B != 0:
                    continue
                phi = val // B
                
                p, q = factor_from_phi(N, phi, k)
                if p and q:
                    print(f"[+] FOUND with k={k}, B={B}, sign={sign}")
                    return p, q, k
        
        # Method 2: Brute force small B
        for B in range(1, 5000):
            for sign in [1, -1]:
                d_approx = (B * phi_approx - sign) // e
                if d_approx <= 0:
                    continue
                
                for delta in range(-5, 6):
                    d = d_approx + delta
                    if d <= 0:
                        continue
                    
                    val = e * d + sign
                    if val % B != 0:
                        continue
                    
                    phi = val // B
                    
                    p, q = factor_from_phi(N, phi, k)
                    if p and q:
                        print(f"[+] FOUND with k={k}, B={B}, sign={sign}, delta={delta}")
                        return p, q, k
    
    return None, None, None

def solve():
    r = remote('65.109.214.93', 13137)
    
    # Get encrypted message
    r.recvuntil(b'[Q]uit')
    r.sendline(b'e')
    line = r.recvline().decode()
    enc_match = re.search(r'enc = (\d+)', line)
    if not enc_match:
        print(f"Failed to parse enc from: {line}")
        return
    enc = int(enc_match.group(1))
    print(f"[*] enc = {enc}")
    
    # Get public parameters
    r.recvuntil(b'[Q]uit')
    r.sendline(b'p')
    line = r.recvline().decode()
    N_match = re.search(r'N = (\d+)', line)
    if not N_match:
        print(f"Failed to parse N from: {line}")
        return
    N = int(N_match.group(1))
    
    line = r.recvline().decode()
    e_match = re.search(r'e = (\d+)', line)
    if not e_match:
        print(f"Failed to parse e from: {line}")
        return
    e = int(e_match.group(1))
    
    print(f"[*] N = {N}")
    print(f"[*] e = {e}")
    
    # Try attack
    p, q, k = attack(N, e, enc)
    
    if p is None:
        print("[-] Attack failed!")
        r.close()
        return
    
    print(f"\n[+] Factored!")
    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    k = {k}")
    
    # Compute phi and decrypt
    phi = (pow(p, k) - 1) * (pow(q, k) - 1)
    d = inverse(e, phi)
    
    m = pow(enc, d, N)
    msg = long_to_bytes(m)
    
    print(f"[*] Decrypted: {msg}")
    
    try:
        msg_str = msg.decode()
        print(f"[*] Message string: {msg_str}")
        
        # Send to server
        r.recvuntil(b'[Q]uit')
        r.sendline(b's')
        r.recvuntil(b'message:')
        r.sendline(msg)
        
        response = r.recvall(timeout=5).decode()
        print(f"\n[*] Server response:\n{response}")
        
        # Extract flag
        flag_match = re.search(r'ASIS\{[^}]+\}', response)
        if flag_match:
            print(f"\n[+] FLAG: {flag_match.group()}")
    except Exception as ex:
        print(f"Error: {ex}")
    
    r.close()

if __name__ == "__main__":
    solve()
