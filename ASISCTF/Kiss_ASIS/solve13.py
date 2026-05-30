#!/usr/bin/env python3
"""
Kiss ASIS - Fixed solver
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd
import sys
from decimal import Decimal, getcontext
getcontext().prec = 100

def analyze_and_solve(N, e, enc):
    """Try to solve given parameters"""
    
    print(f"\n{'='*60}")
    print(f"Analyzing parameters:")
    print(f"N bits: {N.bit_length()}")
    print(f"e bits: {e.bit_length()}")
    print(f"{'='*60}")
    
    # Estimate k based on e/N^k ratios
    print("\nEstimating k based on e/N^k:")
    for k in range(1, 7):
        Nk = N ** k
        Nk_bits = Nk.bit_length()
        e_bits = e.bit_length()
        
        # e/N^k bit difference
        diff = e_bits - Nk_bits
        print(f"  k={k}: e bits - N^{k} bits = {e_bits} - {Nk_bits} = {diff}")
        
        # For k to be correct, e ~ c * N^k where c < 1
        # So e_bits should be close to Nk_bits
        if -5 <= diff <= 5:
            print(f"  --> k={k} looks promising (e ~ N^{k})")
    
    # Check GCD patterns
    print("\nGCD patterns:")
    gcd_patterns = [
        ('N+1', gcd(e, N+1)),
        ('(N+1)^2', gcd(e, (N+1)**2)),
        ('N-1', gcd(e, N-1)),
    ]
    for name, g in gcd_patterns:
        if g > 1:
            print(f"  gcd(e, {name}) = {g}")
    
    # Try Fermat factorization (quick check)
    print("\nTrying Fermat factorization...")
    a = isqrt(N) + 1
    for i in range(1000000):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            p = a - b
            q = a + b
            if p * q == N and p > 1 and q > 1:
                print(f"Fermat found factors!")
                return decrypt_with_factors(p, q, N, e, enc)
        a += 1
        if i % 100000 == 0:
            print(f"  Fermat: {i} iterations...")
    print("  Fermat: no luck")
    
    # Try Pollard rho (quick)
    print("\nTrying Pollard rho...")
    x, y, d = 2, 2, 1
    f = lambda x: (x*x + 1) % N
    for i in range(500000):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x-y), N)
        if d != 1 and d != N:
            print(f"Pollard rho found factor: {d}")
            p = d
            q = N // d
            return decrypt_with_factors(p, q, N, e, enc)
        if i % 100000 == 0:
            print(f"  Pollard rho: {i} iterations...")
    print("  Pollard rho: no luck")
    
    # Try Pollard p-1 with larger bound
    print("\nTrying Pollard p-1...")
    a = 2
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        for _ in range(100):
            a = pow(a, prime, N)
        g = gcd(a - 1, N)
        if 1 < g < N:
            print(f"Pollard p-1 found factor: {g}")
            p = g
            q = N // g
            return decrypt_with_factors(p, q, N, e, enc)
    print("  Pollard p-1: no luck")
    
    # Try Williams p+1
    print("\nTrying Williams p+1...")
    for A in range(3, 20):
        v = A
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            for _ in range(50):
                v = (v*v - 2) % N
        g = gcd(v - 2, N)
        if 1 < g < N:
            print(f"Williams p+1 found factor: {g}")
            p = g
            q = N // g
            return decrypt_with_factors(p, q, N, e, enc)
    print("  Williams p+1: no luck")
    
    print("\nStandard factorization methods failed.")
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
                decoded = msg.decode()
                print(f"k={k}: Decrypted message: {decoded}")
                return decoded
        except Exception as ex:
            print(f"k={k}: Failed - {ex}")
    
    print("Could not decrypt with any k value")
    return None

def main():
    print("="*60)
    print("Kiss ASIS Solver")
    print("="*60)
    
    # Test with sample data first
    print("\nTesting with sample data...")
    
    N_sample = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
    e_sample = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
    enc_sample = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842
    
    result = analyze_and_solve(N_sample, e_sample, enc_sample)
    
    # Try server
    print("\n" + "="*60)
    print("Connecting to server...")
    print("="*60)
    
    try:
        io = remote("65.109.214.93", 13137, timeout=30)
        
        # Get parameters
        io.recvuntil(b"[Q]uit")
        io.sendline(b"p")
        
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        print("Received parameters...")
        
        # Parse N
        for line in data.split("\n"):
            if "N = " in line:
                N = int(line.split("N = ")[1].strip())
            if "e = " in line:
                e = int(line.split("e = ")[1].strip())
        
        # Get encrypted message
        io.sendline(b"e")
        data = io.recvuntil(b"[Q]uit", timeout=10).decode()
        
        for line in data.split("\n"):
            if "enc = " in line:
                enc = int(line.split("enc = ")[1].strip())
        
        print(f"N = {N}")
        print(f"e = {e}")
        print(f"enc = {enc}")
        
        result = analyze_and_solve(N, e, enc)
        
        if result:
            print(f"\nSending secret message: {result}")
            io.sendline(b"s")
            io.recvuntil(b"secret message:")
            io.sendline(result.encode())
            final = io.recvall(timeout=5).decode()
            print(f"Server response: {final}")
        else:
            print("\nCould not solve. Need more advanced techniques.")
        
        io.close()
    except Exception as ex:
        import traceback
        print(f"Error: {ex}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
