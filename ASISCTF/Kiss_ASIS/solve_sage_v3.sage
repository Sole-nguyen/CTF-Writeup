#!/usr/bin/env sage
# -*- coding: utf-8 -*-
"""
Kiss ASIS Solver v3 - SageMath with Lattice attacks
Compatible with SageMath preprocessor (no f-strings)
"""

from sage.all import *
import socket
import re

# PyCryptodome might not be installed in sage env
try:
    from Crypto.Util.number import long_to_bytes
except ImportError:
    def long_to_bytes(n):
        return n.to_bytes((n.bit_length() + 7) // 8, 'big')

HOST = "65.109.214.93"
PORT = 13137

def recv_until(s, marker, timeout_sec=30):
    """Receive data until marker found or timeout"""
    import time
    data = b""
    start = time.time()
    while marker not in data:
        if time.time() - start > timeout_sec:
            raise TimeoutError("recv_until timeout")
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            continue
    return data

def parse_value(data_str, key):
    """Parse 'key = value' from data, return integer or None"""
    # Try regex first
    pattern = key + r"\s*=\s*(\d+)"
    match = re.search(pattern, data_str)
    if match:
        return int(match.group(int(1)))
    # Fallback: line-based parsing
    for line in data_str.split("\n"):
        line = line.strip()
        if line.startswith(key + " =") or line.startswith(key + "="):
            parts = line.split("=", int(1))
            if len(parts) == int(2):
                val_str = parts[int(1)].strip()
                # Extract digits only
                digits = "".join(c for c in val_str if c.isdigit())
                if digits:
                    return int(digits)
    return None

def connect():
    """Connect to server and get parameters"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    # Receive banner
    data = recv_until(s, b"[Q]uit")
    
    # Get encrypted message
    s.send(b"e\n")
    data = recv_until(s, b"[Q]uit")
    data_str = data.decode('utf-8', errors='ignore')
    
    enc = parse_value(data_str, "enc")
    if enc is None:
        # Debug: print what we received
        print("[DEBUG] Failed to parse enc from:")
        print(data_str[:500])
        raise ValueError("Could not parse enc")
    
    # Get public key
    s.send(b"p\n")
    data = recv_until(s, b"[Q]uit")
    data_str = data.decode('utf-8', errors='ignore')
    
    N = parse_value(data_str, "N")
    e = parse_value(data_str, "e")
    
    if N is None or e is None:
        print("[DEBUG] Failed to parse N or e from:")
        print(data_str[:500])
        raise ValueError("Could not parse N or e")
    
    return s, N, e, enc

def send_message(s, msg):
    """Send decrypted message to server"""
    s.send(b"s\n")
    try:
        data = recv_until(s, b"message:", timeout_sec=5)
    except:
        data = recv_until(s, b":", timeout_sec=5)
    
    s.send(msg.encode() + b"\n")
    s.settimeout(5)
    try:
        response = s.recv(4096).decode('utf-8', errors='ignore')
    except:
        response = ""
    return response

def estimate_k(N, e):
    """
    Estimate k from e size.
    phi_k ≈ N^k, so e < N^k means k = ceil(log(e)/log(N))
    """
    nbits = Integer(N).nbits()
    ebits = Integer(e).nbits()
    
    # k is the smallest integer such that e < N^k
    # i.e., e_bits < k * N_bits
    # So k = ceil(e_bits / N_bits)
    k_est = (ebits + nbits - 1) // nbits  # ceiling division
    
    return max(1, min(6, k_est))

def factor_from_sum(N, S):
    """Given N = p*q and S = p+q, find p and q."""
    discriminant = S*S - 4*N
    if discriminant < 0:
        return None, None
    
    sqrt_disc = isqrt(discriminant)
    if sqrt_disc * sqrt_disc != discriminant:
        return None, None
    
    p = (S + sqrt_disc) // 2
    q = (S - sqrt_disc) // 2
    
    if p * q == N:
        return int(p), int(q)
    return None, None

def attack_k1_phi_approx(N, e, enc, max_correction=50000):
    """
    For k=1: e ≈ phi/2, so 2e ≈ phi = N - S + 1
    Therefore: S ≈ N - 2*e + 1
    """
    print("[*] Trying phi approximation attack for k=1...")
    
    base_S = N - 2*e + 1
    
    for correction in range(-max_correction, max_correction + 1):
        S = base_S + correction
        
        if S <= 0 or S >= N:
            continue
        
        p, q = factor_from_sum(N, S)
        
        if p is not None and q is not None:
            print("[!] Factored N! correction = " + str(correction))
            print("    p = " + str(p)[:50] + "...")
            print("    q = " + str(q)[:50] + "...")
            
            phi = (p - 1) * (q - 1)
            
            if gcd(e, phi) != 1:
                print("    gcd(e, phi) != 1, trying next...")
                continue
            
            d_decrypt = inverse_mod(e, phi)
            m = power_mod(enc, d_decrypt, N)
            
            try:
                msg_bytes = long_to_bytes(int(m))
                if all(32 <= b < 127 for b in msg_bytes) and len(msg_bytes) >= 14:
                    msg = msg_bytes.decode()
                    print("[!] Decrypted message: " + msg)
                    return msg
            except:
                pass
    
    print("    failed")
    return None

def attack_lattice_k1(N, e, enc):
    """Lattice attack for k=1 using LLL."""
    print("[*] Trying lattice attack for k=1...")
    
    M = matrix(ZZ, [[e, 1], [N, 0]])
    L = M.LLL()
    
    for row in L:
        d_cand = abs(row[0])
        
        if d_cand > 0 and 1020 <= Integer(d_cand).nbits() <= 1025:
            print("    Trying candidate d with " + str(Integer(d_cand).nbits()) + " bits...")
            
            try:
                m = power_mod(enc, d_cand, N)
                msg_bytes = long_to_bytes(int(m))
                if all(32 <= b < 127 for b in msg_bytes) and len(msg_bytes) >= 14:
                    msg = msg_bytes.decode()
                    print("[!] Lattice attack succeeded!")
                    return msg
            except:
                pass
    
    print("    failed")
    return None

def attack_wiener_variant(N, e, enc):
    """Wiener-style attack with phi approximations."""
    print("[*] Trying Wiener variant attack...")
    
    sqrt_N = isqrt(N)
    
    for S_offset in range(-200, 201):
        S = 2 * sqrt_N + S_offset
        phi_approx = N - S + 1
        
        if phi_approx <= 0:
            continue
        
        cf = continued_fraction(e / phi_approx)
        convergents = cf.convergents()
        
        for conv in convergents[:3000]:
            t_cand = conv.numerator()
            d_cand = conv.denominator()
            
            if d_cand <= 0:
                continue
            
            if Integer(d_cand).nbits() < 1020 or Integer(d_cand).nbits() > 1025:
                continue
            
            for sign in [1, -1]:
                if t_cand == 0:
                    continue
                
                ed = e * d_cand
                if (ed - sign) % t_cand != 0:
                    continue
                    
                phi_cand = (ed - sign) // t_cand
                if phi_cand <= 0:
                    continue
                
                S_cand = N - phi_cand + 1
                p, q = factor_from_sum(N, S_cand)
                
                if p is not None and q is not None:
                    print("[!] Wiener variant found factors!")
                    phi = (p - 1) * (q - 1)
                    
                    if gcd(e, phi) != 1:
                        continue
                        
                    d_decrypt = inverse_mod(e, phi)
                    m = power_mod(enc, d_decrypt, N)
                    
                    try:
                        msg_bytes = long_to_bytes(int(m))
                        if all(32 <= b < 127 for b in msg_bytes):
                            msg = msg_bytes.decode()
                            print("[!] Decrypted: " + msg)
                            return msg
                    except:
                        pass
    
    print("    failed")
    return None

def attack_small_t_k2(N, e, enc, max_t=5000, delta_range=100):
    """
    Attack for k=2: search for small t in e*d = t*phi_2 ± 1
    
    For k=2: phi_2 = (p^2-1)(q^2-1) = (N+1)^2 - S^2
    where S = p + q
    
    Given e*d = t*phi_2 + r (r = ±1):
    d ≈ t * phi_2 / e ≈ t * N^2 / e
    """
    print("[*] Trying small-t attack for k=2 (t up to " + str(max_t) + ")...")
    
    N_sq = Integer(N) * Integer(N)
    N_plus_1_sq = (Integer(N) + 1) ** 2
    
    for t in range(1, max_t + 1):
        if t % 500 == 0:
            print("    t = " + str(t) + "...")
        
        # d ≈ t * N^2 / e
        d_approx = (t * N_sq) // Integer(e)
        
        for delta in range(-delta_range, delta_range + 1):
            d = int(d_approx + delta)
            if d <= 0:
                continue
            
            # Check both e*d - 1 and e*d + 1
            for r in [1, -1]:
                val = Integer(e) * d - r
                
                if val <= 0 or val % t != 0:
                    continue
                
                phi = val // t
                
                # For k=2: phi = (N+1)^2 - S^2
                S_sq = N_plus_1_sq - phi
                
                if S_sq <= 0:
                    continue
                
                S = isqrt(S_sq)
                if S * S != S_sq:
                    continue
                
                # Found valid S, now factor N
                p, q = factor_from_sum(N, S)
                
                if p is not None and q is not None:
                    print("[!] k=2 attack: Found at t=" + str(t) + ", delta=" + str(delta) + ", r=" + str(r))
                    print("    p = " + str(p)[:50] + "...")
                    print("    q = " + str(q)[:50] + "...")
                    
                    # Decrypt with phi_k where k might be 2
                    phi_2 = (p**2 - 1) * (q**2 - 1)
                    
                    if gcd(e, phi_2) != 1:
                        # Try phi_1
                        phi_1 = (p - 1) * (q - 1)
                        if gcd(e, phi_1) == 1:
                            d_decrypt = inverse_mod(e, phi_1)
                            m = power_mod(enc, d_decrypt, N)
                            try:
                                msg = long_to_bytes(int(m)).decode()
                                if all(32 <= ord(c) < 127 for c in msg):
                                    return msg
                            except:
                                pass
                        continue
                    
                    d_decrypt = inverse_mod(e, phi_2)
                    m = power_mod(enc, d_decrypt, N)
                    
                    try:
                        msg = long_to_bytes(int(m)).decode()
                        if all(32 <= ord(c) < 127 for c in msg):
                            print("[!] Decrypted with k=2: " + msg)
                            return msg
                    except:
                        pass
                    
                    # Also try decryption with phi_1
                    phi_1 = (p - 1) * (q - 1)
                    if gcd(e, phi_1) == 1:
                        d_decrypt = inverse_mod(e, phi_1)
                        m = power_mod(enc, d_decrypt, N)
                        try:
                            msg = long_to_bytes(int(m)).decode()
                            if all(32 <= ord(c) < 127 for c in msg):
                                print("[!] Decrypted with k=1: " + msg)
                                return msg
                        except:
                            pass
    
    print("    failed")
    return None

def attack_fermat(N, e, enc, max_iter=200000):
    """Extended Fermat factorization"""
    print("[*] Trying Fermat (" + str(max_iter) + " iterations)...")
    
    a = isqrt(N)
    if a * a < N:
        a += 1
    
    for i in range(max_iter):
        b2 = a*a - N
        b = isqrt(b2)
        if b * b == b2:
            p = int(a + b)
            q = int(a - b)
            if p * q == N and p > 1 and q > 1:
                print("[!] Fermat found factors at iteration " + str(i))
                phi = (p - 1) * (q - 1)
                if gcd(e, phi) == 1:
                    d_decrypt = inverse_mod(e, phi)
                    m = power_mod(enc, d_decrypt, N)
                    try:
                        msg = long_to_bytes(int(m)).decode()
                        if all(32 <= ord(c) < 127 for c in msg):
                            return msg
                    except:
                        pass
        a += 1
    
    print("    failed")
    return None

def attack_gcd_analysis(N, e, enc):
    """GCD-based analysis"""
    print("[*] Trying GCD analysis...")
    
    g = gcd(e, N - 1)
    if g > 1:
        print("    gcd(e, N-1) = " + str(g))
        
        for d in divisors(g)[:100]:
            if d <= 1:
                continue
            candidate = gcd(d, N)
            if 1 < candidate < N:
                p = int(candidate)
                q = int(N // p)
                print("[!] GCD found factor!")
                
                phi = (p - 1) * (q - 1)
                if gcd(e, phi) == 1:
                    d_decrypt = inverse_mod(e, phi)
                    m = power_mod(enc, d_decrypt, N)
                    try:
                        msg = long_to_bytes(int(m)).decode()
                        if all(32 <= ord(c) < 127 for c in msg):
                            return msg
                    except:
                        pass
    
    print("    no useful gcd found")
    return None

def main():
    print("=" * 60)
    print("Kiss ASIS - SageMath Solver v3")
    print("=" * 60)
    
    max_attempts = 100
    
    for attempt in range(1, max_attempts + 1):
        try:
            print("\n" + "=" * 60)
            print("[Attempt " + str(attempt) + "/" + str(max_attempts) + "]")
            
            s, N, e, enc = connect()
            k_est = estimate_k(N, e)
            
            print("  N: " + str(Integer(N).nbits()) + " bits")
            print("  e: " + str(Integer(e).nbits()) + " bits")
            print("  k (estimated): " + str(k_est))
            
            result = None
            
            if k_est == 2:
                print("  [*] k=2 detected - trying small-t attack...")
                result = attack_small_t_k2(N, e, enc, 3000, 50)
                if not result:
                    result = attack_fermat(N, e, enc, 100000)
            elif k_est > 2:
                print("  [*] k=" + str(k_est) + " - trying Fermat only...")
                result = attack_fermat(N, e, enc, 100000)
            else:
                print("  [*] k=1 detected - trying all attacks...")
                
                result = attack_k1_phi_approx(N, e, enc, 100000)
                
                if not result:
                    result = attack_gcd_analysis(N, e, enc)
                
                if not result:
                    result = attack_wiener_variant(N, e, enc)
                
                if not result:
                    result = attack_lattice_k1(N, e, enc)
                
                if not result:
                    result = attack_fermat(N, e, enc, 200000)
            
            if result:
                print("\n[!!!] SUCCESS!")
                print("[!!!] Message: " + result)
                response = send_message(s, result)
                print("[!!!] Server response: " + response)
                
                if "flag" in response.lower() or "ASIS" in response:
                    print("\n" + "=" * 60)
                    print("FLAG CAPTURED!")
                    print("=" * 60)
                    return
            else:
                print("  [-] All attacks failed")
            
            s.close()
            
        except KeyboardInterrupt:
            print("\n[!] Interrupted")
            break
        except Exception as ex:
            print("  [!] Error: " + str(ex))
            import traceback
            traceback.print_exc()
            continue
    
    print("\n[*] Finished all attempts")

if __name__ == "__main__":
    main()
