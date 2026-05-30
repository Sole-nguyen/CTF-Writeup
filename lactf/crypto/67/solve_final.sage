#!/usr/bin/env sage

n = 1901525731783172416203839378671587214422745380133137208536437412068131541758277290328801163521119197746682203400123662482260820744052033622063647039210426245822869187002067017948483048223604232501724823854436609856443113104852812365571212878100652199402375584728570249179997361195244269332600766309836419809559207417005760425094596123877239496837743699796158805966879382962588782321510484138949668604001
c = 1252492969959188673736313237122046152105325519348455143424695915309270725508605651140132440646734872638727292815680972964911252437780394621254251486827749378723860527268151373384404572271341490254359623613970737005552807521806214056991581569507310664954744406683220443652006709831938903185296438772482818881934209107697305594352071483991205295203938894133819639837350546169532296608367131787790924175474
e = 65537
L = 67

high_part = int("6" * L) * (10**(2 * L))
low_part = int("7" * L)
known_p = high_part + low_part

print(f"known_p = {known_p}")
print(f"n bits: {Integer(n).nbits()}")
print()

P.<x> = PolynomialRing(Zmod(n))
f = x * (10^L) + known_p
f = f.monic()

print("Attempting to solve for root with Coppersmith...")
print(f"X bound: {10^L}")
print(f"beta: 0.45")
print()

roots = f.small_roots(X=10^L, beta=0.45)

if roots:
    print(f"Found {len(roots)} root(s)!")
    x_sol = int(roots[0])
    print(f"Recovered middle part: {x_sol}")
    
    p = x_sol * (10^L) + known_p
    print(f"p = {p}")
    
    if n % p == 0:
        print("\n✓ Success! Found prime factor p.")
        q = n // p
        print(f"q = {q}")
        
        phi = (p - 1) * (q - 1)
        d = inverse_mod(e, phi)
        m = pow(c, d, n)
        
        from Crypto.Util.number import long_to_bytes
        flag = long_to_bytes(int(m))
        print(f"\nFLAG: {flag.decode()}")
    else:
        print("Root found but does not factor n.")
else:
    print("No roots found with beta=0.45")
    print("Trying beta=0.4...")
    
    roots = f.small_roots(X=10^L, beta=0.4)
    if roots:
        print(f"Found {len(roots)} root(s) with beta=0.4!")
        x_sol = int(roots[0])
        p = x_sol * (10^L) + known_p
        
        if n % p == 0:
            q = n // p
            phi = (p - 1) * (q - 1)
            d = inverse_mod(e, phi)
            m = pow(c, d, n)
            
            from Crypto.Util.number import long_to_bytes
            flag = long_to_bytes(int(m))
            print(f"\nFLAG: {flag.decode()}")
    else:
        print("Still no solution found.")
