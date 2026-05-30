#!/usr/bin/env python3
"""
Kiss ASIS - RSA with weak key generation
The weakness: phi = (p^k - 1)(q^k - 1) and e*d ≡ ±1 (mod phi)
With d ≈ N and k > 1, we have e*d ± 1 ≈ phi, so we can factor.
"""

from pwn import *
from Crypto.Util.number import *
from math import gcd, isqrt
from sympy import factorint, divisors
import re

def solve_quadratic_mod(a, b, c, n):
    """Solve ax^2 + bx + c = 0 mod n, returns integer roots"""
    # For our case, we're looking for integer solutions
    disc = b*b - 4*a*c
    if disc < 0:
        return []
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return []
    roots = []
    for sign in [1, -1]:
        num = -b + sign * sqrt_disc
        if num % (2*a) == 0:
            roots.append(num // (2*a))
    return roots

def factor_from_pk_qk(pk_minus_1, qk_minus_1, N, k):
    """
    Given (p^k - 1) and (q^k - 1), try to recover p and q
    We know p^k = pk_minus_1 + 1, so we need to find the k-th root
    """
    pk = pk_minus_1 + 1
    qk = qk_minus_1 + 1
    
    # Try to find p = pk^(1/k)
    p = round(pk ** (1/k))
    for delta in range(-10, 11):
        pp = p + delta
        if pp > 1 and pp ** k == pk:
            q = N // pp
            if pp * q == N and isPrime(pp) and isPrime(q):
                return pp, q
    return None, None

def try_factor_phi(phi_candidate, N, k):
    """
    phi = (p^k - 1)(q^k - 1) = p^k * q^k - p^k - q^k + 1
    Let X = p^k, Y = q^k
    X * Y = N^k
    X + Y = N^k + 1 - phi
    So X and Y are roots of: t^2 - (N^k + 1 - phi)*t + N^k = 0
    """
    Nk = N ** k
    sum_XY = Nk + 1 - phi_candidate
    prod_XY = Nk
    
    # t^2 - sum_XY * t + prod_XY = 0
    disc = sum_XY * sum_XY - 4 * prod_XY
    if disc < 0:
        return None, None
    
    sqrt_disc = isqrt(disc)
    if sqrt_disc * sqrt_disc != disc:
        return None, None
    
    X = (sum_XY + sqrt_disc) // 2
    Y = (sum_XY - sqrt_disc) // 2
    
    if X * Y != prod_XY:
        return None, None
    
    # Now X = p^k, Y = q^k
    # Find k-th roots
    for pk, qk in [(X, Y), (Y, X)]:
        p = round(pk ** (1/k))
        for delta in range(-5, 6):
            pp = p + delta
            if pp > 1 and pp ** k == pk:
                q = N // pp
                if pp * q == N:
                    if isPrime(pp) and isPrime(q):
                        return min(pp, q), max(pp, q)
    
    return None, None

def attack(N, e, enc):
    """Main attack: try different values of k and t"""
    print(f"[*] N bits: {N.bit_length()}")
    print(f"[*] e bits: {e.bit_length()}")
    
    # e is much larger than N, suggesting k > 1
    # e*d ± 1 = t * phi where t is small
    
    for k in range(1, 7):
        print(f"\n[*] Trying k = {k}")
        
        # phi = (p^k - 1)(q^k - 1) ≈ N^k for large k
        # e * d ≈ phi, and d ≈ N
        # So e ≈ N^(k-1)
        
        expected_e_bits = N.bit_length() * (k - 1) if k > 1 else N.bit_length()
        print(f"    Expected e bits for k={k}: ~{expected_e_bits}")
        
        if k == 1:
            # For k=1, e*d ≈ phi ≈ N, but e is huge, so skip
            if e.bit_length() > N.bit_length() + 10:
                print(f"    e too large for k=1, skipping")
                continue
        
        # Try small values of t
        for t in range(1, 20):
            for sign in [1, -1]:
                # e*d = t * phi + sign
                # We don't know d, but we know d is about D * n_bits
                # Actually, we can compute phi candidates from e*d
                
                # Since d ≈ N (D ≈ 0.999), let's estimate d
                # e*d ≈ e * N^0.999
                # phi = (e*d - sign) / t
                
                # But we need to guess d more precisely...
                # Actually, for the attack: if e*d = t*phi ± 1
                # and phi = (p^k-1)(q^k-1), we can work with:
                # 
                # For small t, we can try: assume t=1
                # Then phi ≈ e*d, and since d < N, phi < e*N
                # 
                # Better approach: use continued fractions on e/N^k
                pass
        
        # Alternative: Direct approach for t=1
        # Assume e*d = phi + 1 or e*d = phi - 1
        # We need to find d such that (e*d ± 1) factors nicely
        
        # For k=2: phi = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)
        # e*d ≈ N^2, and d ≈ N, so e ≈ N
        
        # Let's try a different approach:
        # Use the relation e*d ≡ ±1 (mod phi)
        # This means e*d = k*phi ± 1 for some small k
        
        # Wiener-like attack for large d:
        # When d is large, e*d ≈ phi, so e/phi ≈ 1/d
        # But we don't know phi...
        
        # However, phi = (p^k-1)(q^k-1) and N = p*q
        # So phi ≈ N^k (approximately)
        
        # Let's try: e ≈ N^k / d ≈ N^(k-1) since d ≈ N
        
        # For k where e ≈ N^(k-1):
        ratio = e.bit_length() / N.bit_length()
        estimated_k = round(ratio) + 1
        print(f"    e/N bit ratio: {ratio:.2f}, estimated k: {estimated_k}")
        
        if k == estimated_k:
            print(f"    [!] k={k} matches estimation!")
            
            # Now, assume e*d = phi ± 1 (t=1)
            # phi = (p^k - 1)(q^k - 1)
            # We need to find d
            
            # Since D ≈ 0.999, d has about 1023-1024 bits
            # e*d ≈ N^k = N^2 for k=2
            
            # For t=1: e*d = phi ± 1
            # d = (phi ± 1) / e
            # phi = (p^k - 1)(q^k - 1) where p*q = N
            
            # Let's use: e*d - 1 = phi or e*d + 1 = phi
            # and solve for p, q
            
            # Approach: enumerate possible d values
            # d is a prime with about 1023 bits (D * 1024 ≈ 1023)
            
            # Actually, let's think differently:
            # e * d ≡ s (mod phi) where s = ±1
            # e * d = k * phi + s
            # 
            # phi = (p^k - 1)(q^k - 1)
            # 
            # For k=2:
            # phi = (p^2-1)(q^2-1) = (p-1)(p+1)(q-1)(q+1)
            #
            # If k_mult = 1:
            # e * d = phi ± 1
            # 
            # Trying small k_mult values:
            for k_mult in range(1, 10):
                for s in [1, -1]:
                    # e * d = k_mult * phi + s
                    # phi = (e*d - s) / k_mult
                    
                    # We need to find d. 
                    # d has dbit = int(1024 * D) + 1 where D ∈ [0.999, 0.9999]
                    # So dbit ∈ [1023, 1024]
                    
                    # Let's estimate: d ≈ N (roughly)
                    # So phi ≈ (e * N - s) / k_mult
                    
                    estimated_phi = (e * N) // k_mult
                    
                    # Now check if this phi could factor as (p^k-1)(q^k-1)
                    p, q = try_factor_phi(estimated_phi, N, k)
                    if p and q:
                        print(f"    [+] Found factors with k={k}, k_mult={k_mult}, s={s}!")
                        print(f"        p = {p}")
                        print(f"        q = {q}")
                        return p, q
                    
                    # Also try with actual d being prime
                    # d should satisfy: e*d ≡ s (mod phi) and d is prime
                    # 
                    # For each possible phi, check if d = (k_mult * phi + s) / e is integer and prime
                    # But we need phi first...
    
    # Alternative approach: Boneh-Durfee or similar for large d
    # When e*d ≈ phi, we have e/phi ≈ 1/d
    # Continued fractions on e/N^k might give us something
    
    print("\n[*] Trying continued fractions approach...")
    for k in range(1, 7):
        Nk = pow(N, k)
        
        # e/Nk ≈ d^(-1) when e*d ≈ Nk
        from fractions import Fraction
        
        # Use convergents of e/Nk
        cf = []
        a, b = e, Nk
        while b:
            cf.append(a // b)
            a, b = b, a % b
            if len(cf) > 200:
                break
        
        # Check convergents
        p_prev, p_curr = 0, 1
        q_prev, q_curr = 1, 0
        
        for i, c in enumerate(cf[:100]):
            p_prev, p_curr = p_curr, c * p_curr + p_prev
            q_prev, q_curr = q_curr, c * q_curr + q_prev
            
            # p_curr/q_curr is a convergent
            # If e/Nk ≈ 1/d, then q_curr might be close to d
            
            # Check if q_curr could be d
            d_candidate = q_curr
            if d_candidate < 2:
                continue
            
            for t in range(1, 5):
                for s in [1, -1]:
                    phi_candidate = (e * d_candidate - s) // t
                    if (e * d_candidate - s) % t != 0:
                        continue
                    
                    p, q = try_factor_phi(phi_candidate, N, k)
                    if p and q:
                        print(f"[+] Found via CF! k={k}, convergent {i}")
                        print(f"    d = {d_candidate}")
                        print(f"    p = {p}")
                        print(f"    q = {q}")
                        return p, q
    
    return None, None

def decrypt_rsa(c, d, N):
    """Standard RSA decryption"""
    return pow(c, d, N)

def connect_and_solve():
    """Connect to server and solve"""
    # r = remote('65.109.214.93', 13137)
    r = remote('65.109.214.93', 13137)
    
    # Get encrypted message
    r.recvuntil(b'[Q]uit')
    r.sendline(b'e')
    line = r.recvline().decode()
    enc = int(re.search(r'enc = (\d+)', line).group(1))
    print(f"[*] enc = {enc}")
    
    # Get public parameters
    r.recvuntil(b'[Q]uit')
    r.sendline(b'p')
    line = r.recvline().decode()
    N = int(re.search(r'N = (\d+)', line).group(1))
    line = r.recvline().decode()
    e = int(re.search(r'e = (\d+)', line).group(1))
    print(f"[*] N = {N}")
    print(f"[*] e = {e}")
    
    # Attack
    p, q = attack(N, e, enc)
    
    if p is None:
        print("[-] Attack failed!")
        r.close()
        return
    
    print(f"\n[+] Factored N!")
    print(f"    p = {p}")
    print(f"    q = {q}")
    
    # Now we need to find d and decrypt
    # We need to figure out which k was used
    for k in range(1, 7):
        phi = (pow(p, k) - 1) * (pow(q, k) - 1)
        
        # Check both r=0 and r=1 cases
        for r_val in [0, 1]:
            try:
                # e*d ≡ (-1)^r (mod phi)
                # So d = (-1)^r * inverse(e, phi) mod phi
                if r_val == 0:
                    d = inverse(e, phi)
                else:
                    d = phi - inverse(e, phi)
                
                # Try to decrypt
                m = decrypt_rsa(enc, d, N)
                msg = long_to_bytes(m)
                
                # Check if it's printable
                try:
                    msg_str = msg.decode('latin-1')
                    if all(32 <= ord(c) <= 126 for c in msg_str):
                        print(f"\n[+] Decrypted message (k={k}, r={r_val}):")
                        print(f"    {msg_str}")
                        
                        # Send the message
                        r.recvuntil(b'[Q]uit')
                        r.sendline(b's')
                        r.recvuntil(b'message:')
                        r.sendline(msg)
                        
                        response = r.recvall(timeout=5).decode()
                        print(f"\n[*] Server response:\n{response}")
                        
                        if 'ASIS{' in response:
                            flag = re.search(r'ASIS\{[^}]+\}', response)
                            if flag:
                                print(f"\n[+] FLAG: {flag.group()}")
                        
                        return msg_str
                except:
                    pass
            except:
                pass
    
    r.close()
    return None

if __name__ == "__main__":
    # Test with the provided example first
    N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
    e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
    enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842
    
    print("[*] Testing with provided values...")
    p, q = attack(N, e, enc)
    
    if p:
        print(f"\n[+] Now connecting to server...")
        connect_and_solve()
    else:
        print("\n[*] Trying direct connection...")
        connect_and_solve()
