#!/usr/bin/env python3
"""
Kiss ASIS - Connect to server and try to solve
"""

from pwn import *
from Crypto.Util.number import *
from math import isqrt, gcd

def solve_instance(N, e, enc):
    """Try to solve given instance"""
    
    print(f"N bits: {N.bit_length()}")
    print(f"e bits: {e.bit_length()}")
    
    # Check GCD patterns
    g_Np1_sq = gcd(e, (N+1)**2)
    g_N2m1 = gcd(e, N**2 - 1)
    print(f"gcd(e, (N+1)^2) = {g_Np1_sq}")
    print(f"gcd(e, N^2-1) = {g_N2m1}")
    
    # Calculate e/N^2 ratio
    ratio = e / (N**2)
    print(f"e/N^2 = {ratio:.6f}")
    
    # Try Fermat factorization (in case p, q are close)
    print("\nTrying Fermat factorization...")
    a = isqrt(N) + 1
    for i in range(100000):
        b2 = a*a - N
        b = isqrt(b2)
        if b*b == b2:
            p = a - b
            q = a + b
            print(f"Found! p = {p}, q = {q}")
            
            # Try decryption for all k
            for k in range(1, 7):
                try:
                    phi = (p**k - 1) * (q**k - 1)
                    d = inverse(e, phi)
                    m = pow(enc, d, N)
                    msg = long_to_bytes(m)
                    if all(32 <= c <= 126 for c in msg):
                        print(f"k={k}: {msg}")
                        return msg.decode()
                except:
                    pass
            break
        a += 1
    
    # Try continued fractions on e/N^k for various k
    print("\nTrying continued fractions...")
    for k_exp in [1, 2, 3]:
        Nk = N ** k_exp
        
        # Get continued fraction of e/N^k
        num, den = e, Nk
        h0, h1 = 0, 1
        k0, k1 = 1, 0
        
        for _ in range(1000):
            if den == 0:
                break
            q = num // den
            num, den = den, num - q * den
            
            h2 = q * h1 + h0
            k2 = q * k1 + k0
            
            t_cand, d_cand = h2, k2
            
            if d_cand > 0 and 1000 < d_cand.bit_length() < 1030:
                # Check if this could be valid
                for eps in [1, -1]:
                    val = e * d_cand - eps
                    if val > 0 and val % t_cand == 0:
                        phi = val // t_cand
                        
                        # Try to factor N using phi
                        if k_exp == 1:
                            S = N + 1 - phi
                            if S > 0:
                                disc = S*S - 4*N
                                if disc >= 0:
                                    sqrt_disc = isqrt(disc)
                                    if sqrt_disc * sqrt_disc == disc:
                                        p = (S + sqrt_disc) // 2
                                        q = (S - sqrt_disc) // 2
                                        if p * q == N:
                                            print(f"Found via CF! k={k_exp}")
                                            d = inverse(e, phi)
                                            m = pow(enc, d, N)
                                            return long_to_bytes(m).decode()
            
            h0, h1 = h1, h2
            k0, k1 = k1, k2
    
    print("Could not solve this instance")
    return None

def main():
    # Try local first with the sample data
    print("="*60)
    print("Testing with sample data")
    print("="*60)
    
    N = 66627682657033480168920187774700338099119163894700639867559793711852321323194956934561956009699483456352759336740646362330656682548123019706093978419915461291405285982978411974382545915202657291635172181989688542082281348542601893964276986797147623821066126309413103802877238347144875198855870571309698661809
    e = 3444284678354053524331804498049069615717524803523963300854615135909117396826537590933646882422789044489120659830437490853940254161855138707785259934160149209481592077842288180204607265246193733324338068580955458694338735401875160209656581805824469176991774124369956121556417975707133426344474165685466043099263647103979596583530646578707225521708055694093229999985757961280298569389187395343635703900836560006653837229625128010163370539638837959292391120670308563471744193029911930728199024838412817763941898426510771943359175058678066474258493468986570343076539835638220598742652757028196067323075193353595684112451
    enc = 19049843608207763655692810838063554436154062262108712725877949919619642183745172100846516946273082384984939717303733556691744416298826595557856112858629786249293870623921393396947962378504877871589074114550944762174778508474025158023917620419456294711767629711134839372141010679298572210087693599337137008842
    
    result = solve_instance(N, e, enc)
    if result:
        print(f"\nDecrypted: {result}")
    
    # Now try connecting to server
    print("\n" + "="*60)
    print("Connecting to server...")
    print("="*60)
    
    try:
        io = remote("65.109.214.93", 13137, timeout=30)
        
        # Receive data
        data = io.recvuntil(b"enc = ").decode()
        data += io.recvline().decode()
        
        print(data)
        
        # Parse
        lines = data.strip().split('\n')
        for line in lines:
            if line.startswith('N = '):
                N = int(line.split(' = ')[1])
            elif line.startswith('e = '):
                e = int(line.split(' = ')[1])
            elif line.startswith('enc = '):
                enc = int(line.split(' = ')[1])
        
        result = solve_instance(N, e, enc)
        if result:
            print(f"\nSending: {result}")
            io.sendline(result.encode())
            
            # Get flag
            response = io.recvall(timeout=5)
            print(response.decode())
        
        io.close()
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()
