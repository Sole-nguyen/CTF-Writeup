#!/usr/bin/env python3
"""
Kiss ASIS Solver v22 - LLL-based attack for k=1 cases

Uses pure Python LLL (olll) to try lattice-based attacks.

Key relationship for k=1:
e * d = ±1 + t * phi(N)
e * d ≈ ±1 + t * (N - S)  where S = p + q ≈ 2*sqrt(N)

Rearranging:
e * d - t * N ≈ ±1 - t * S

We can build a lattice to find (d, t) such that:
|e*d - t*N| is small (order of t*sqrt(N))
"""

from pwn import remote, context
import olll
from math import isqrt, gcd
from Crypto.Util.number import long_to_bytes, inverse
import json
from fractions import Fraction

context.log_level = 'error'

HOST = "65.109.214.93"
PORT = 13137

def get_params():
    """Connect and get N, e, enc from server"""
    io = remote(HOST, PORT)
    
    # Get encrypted message
    io.recvuntil(b'[Q]uit')
    io.sendline(b'e')
    line = io.recvline().decode()
    # Parse enc = <value>
    if 'enc = ' in line:
        enc = int(line.split('enc = ')[1])
    else:
        raise ValueError(f"Could not parse enc from: {line}")
    
    # Get public key
    io.recvuntil(b'[Q]uit')
    io.sendline(b'p')
    line1 = io.recvline().decode()
    line2 = io.recvline().decode()
    
    # Parse N and e
    if 'N = ' in line1:
        N = int(line1.split('N = ')[1])
    else:
        raise ValueError(f"Could not parse N from: {line1}")
    
    if 'e = ' in line2:
        e = int(line2.split('e = ')[1])
    else:
        raise ValueError(f"Could not parse e from: {line2}")
    
    return io, N, e, enc

def estimate_k(N, e):
    """Estimate k from ratio e/N^k"""
    nbits = N.bit_length()
    ebits = e.bit_length()
    k_est = round(ebits / nbits)
    if k_est < 1:
        k_est = 1
    elif k_est > 6:
        k_est = 6
    return k_est

def continued_fraction_convergents(num, den, max_convergents=10000):
    """Generate convergents of num/den"""
    convergents = []
    a = num // den
    p_prev, p_curr = 1, a
    q_prev, q_curr = 0, 1
    convergents.append((p_curr, q_curr))
    
    num, den = den, num - a * den
    
    while den != 0 and len(convergents) < max_convergents:
        a = num // den
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
        convergents.append((p_curr, q_curr))
        num, den = den, num - a * den
    
    return convergents

def lll_attack_k1(N, e, enc):
    """
    LLL-based attack for k=1 case.
    
    e * d = ±1 + t * phi
    e * d ≈ t * N (since phi ≈ N and ed is large)
    
    So t/d ≈ e/N
    
    But we want d directly. Let's try a different formulation.
    
    Since d is prime and ~1024 bits, we can't enumerate.
    
    Let's use the lattice:
    [1  0  e]
    [0  1  N]
    
    Short vectors (a, b) give a*e + b*N small.
    If we find (d, -t) where |d*e - t*N| is small, we get d.
    
    But d ~ N so (d, t) is not a short vector...
    """
    # First, try enhanced continued fractions
    # with better approximation of phi
    
    # For k=1: phi = (p-1)(q-1) = N - (p+q) + 1
    # p + q ≈ 2*sqrt(N), so phi ≈ N - 2*sqrt(N)
    
    sqrt_N = isqrt(N)
    
    # Try various approximations of phi
    for delta in range(-100, 101):
        S_approx = 2 * sqrt_N + delta
        phi_approx = N - S_approx + 1
        
        # In our case: e*d = 1 + t*phi or e*d = -1 + t*phi
        # So e*d/phi ≈ t (integer)
        # And d/phi ≈ t/e
        # So (e*d - 1)/phi = t or (e*d + 1)/phi = t
        
        # Rearranging: d = (1 + t*phi)/e or d = (-1 + t*phi)/e
        
        # t ≈ e*d/phi. Since d < phi typically, t < e.
        # More precisely, t = (e*d ± 1)/phi
        # Since e ≈ phi/2 for k=1, and d ≈ phi, we get t ≈ d/2
        
        # Let's use CF on e/phi_approx to find t/d candidates
        convergents = continued_fraction_convergents(e, phi_approx, 5000)
        
        for t_cand, d_cand in convergents:
            if d_cand == 0:
                continue
            
            # Check if this could be our d
            # d should be prime and ~1024 bits
            if d_cand.bit_length() < 1020 or d_cand.bit_length() > 1025:
                continue
            
            # Check gcd condition
            if gcd(e, d_cand) != 1:
                continue
            
            # Try decryption
            try:
                # If e*d ≡ 1 (mod phi), then d_decrypt = d mod phi
                # But we need d_decrypt = e^{-1} mod phi_actual
                # If d_cand is correct and e*d_cand ≡ 1 (mod phi_actual),
                # then we can use d_cand directly
                m = pow(enc, d_cand, N)
                try:
                    msg = long_to_bytes(m)
                    if all(32 <= b < 127 for b in msg) and len(msg) >= 14:
                        return msg.decode()
                except:
                    pass
            except:
                pass
    
    return None

def lll_2d_attack(N, e, enc):
    """
    Try 2D LLL lattice attack.
    
    Build lattice basis:
    [1,   0]
    [e,   N]
    
    LLL will find short vectors.
    """
    # Scale factors for LLL
    # We want to find (d, t) such that d*1 + t*e ≈ 0 mod N is small
    # Hmm, this doesn't directly work for our case.
    
    # Different formulation:
    # e * d = 1 + t * phi
    # Let's say phi ≈ N (close enough for k=1)
    # Then e * d ≈ 1 + t * N
    # So e * d - t * N ≈ 1
    
    # Lattice: [e  1]
    #          [N  0]
    # Short vector (d, -t) gives (d*e - t*N, d) close to (1, d)
    # But d ~ N so this isn't "short" in lattice sense
    
    # Let's try anyway with scaling
    B = [[e, 1], [N, 0]]
    
    try:
        L = olll.reduction(B)
        for v in L:
            d_cand = abs(v[0])
            residue = abs(v[1])
            
            if d_cand > 0 and d_cand.bit_length() >= 1020 and d_cand.bit_length() <= 1025:
                # Try as d
                try:
                    m = pow(enc, d_cand, N)
                    msg = long_to_bytes(m)
                    if all(32 <= b < 127 for b in msg) and len(msg) >= 14:
                        return msg.decode()
                except:
                    pass
    except Exception as ex:
        print(f"LLL error: {ex}")
    
    return None

def try_low_private_exponent_variants(N, e, enc):
    """
    Wiener-style attack with different phi approximations
    """
    sqrt_N = isqrt(N)
    
    # For k=1: ed ≡ ±1 (mod phi), phi = (p-1)(q-1)
    # e ≈ N/2 (observed from samples)
    # d ≈ N (large)
    
    # Standard Wiener fails because d > N^0.25
    
    # But we can try: since e*d = ±1 + t*phi,
    # and for k=1, e ≈ phi/2, d ≈ phi, so t ≈ (e*d)/phi ≈ d/2
    
    # Let's enumerate possible relationships:
    # If e is close to phi/2, then 2e ≈ phi
    # So phi = 2e + small_correction
    
    for correction in range(-1000, 1001):
        phi_approx = 2 * e + correction
        
        if phi_approx <= 0:
            continue
            
        # Check if this phi_approx is consistent with N
        # phi = N - S + 1, so S = N - phi + 1
        S_implied = N - phi_approx + 1
        
        # S = p + q, so p and q are roots of x^2 - Sx + N = 0
        discriminant = S_implied * S_implied - 4 * N
        
        if discriminant < 0:
            continue
            
        sqrt_disc = isqrt(discriminant)
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # Found valid S!
        p = (S_implied + sqrt_disc) // 2
        q = (S_implied - sqrt_disc) // 2
        
        if p * q != N:
            continue
        
        # We factored N!
        print(f"[!] Factored N with correction={correction}")
        print(f"    p = {p}")
        print(f"    q = {q}")
        
        phi_actual = (p - 1) * (q - 1)
        
        if gcd(e, phi_actual) != 1:
            print(f"    gcd(e, phi) = {gcd(e, phi_actual)} != 1, skipping")
            continue
        
        d_decrypt = inverse(e, phi_actual)
        m = pow(enc, d_decrypt, N)
        
        try:
            msg = long_to_bytes(m)
            if all(32 <= b < 127 for b in msg):
                return msg.decode()
        except:
            pass
    
    return None

def main():
    print("Kiss ASIS LLL Solver v22")
    print("=" * 60)
    
    max_attempts = 100
    
    for attempt in range(1, max_attempts + 1):
        try:
            io, N, e, enc = get_params()
            k_est = estimate_k(N, e)
            
            print(f"\n[Attempt {attempt}/{max_attempts}]")
            print(f"  N: {N.bit_length()} bits, e: {e.bit_length()} bits, k~{k_est}")
            
            # Only focus on k=1 cases for lattice attacks
            if k_est != 1:
                print("  [*] Skipping (not k=1)")
                io.close()
                continue
            
            # Try low private exponent variants first (fastest)
            print("  [*] Trying phi approximation attack...")
            result = try_low_private_exponent_variants(N, e, enc)
            
            if result:
                print(f"\n[!!!] FOUND MESSAGE: {result}")
                io.recvuntil(b'[Q]uit')
                io.sendline(b's')
                io.recvuntil(b'message:')
                io.sendline(result.encode())
                response = io.recvall(timeout=5).decode()
                print(response)
                
                if 'flag' in response.lower() or 'asis' in response.lower():
                    print(f"\n[FLAG FOUND]")
                    return
                
                io.close()
                continue
            
            print("    failed")
            
            # Try enhanced CF attack
            print("  [*] Trying enhanced CF attack...")
            result = lll_attack_k1(N, e, enc)
            
            if result:
                print(f"\n[!!!] FOUND MESSAGE: {result}")
                io.recvuntil(b'[Q]uit')
                io.sendline(b's')
                io.recvuntil(b'message:')
                io.sendline(result.encode())
                response = io.recvall(timeout=5).decode()
                print(response)
                io.close()
                continue
            
            print("    failed")
            
            io.close()
            
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            break
        except Exception as ex:
            print(f"  [!] Error: {ex}")
            continue
    
    print("\n[*] Finished all attempts")

if __name__ == "__main__":
    main()
