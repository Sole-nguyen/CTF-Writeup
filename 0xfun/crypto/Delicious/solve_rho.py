from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
from sympy.ntheory.modular import crt
import random

# Parse the output
samples = [
    (227293414901, 1559214942312, 3513364021163),
    (2108076514529, 1231299005176, 2627609083643),
    (1752240335858, 1138499826278, 2917520243087),
    (1564551923739, 283918762399, 2602533803279),
    (1809320390770, 700655135118, 2431482961679),
    (1662077312271, 354214090383, 2820691962743),
    (474213905602, 1149389382916, 3525049671887),
    (2013522313912, 2559608094485, 2679851241659),
]

ct = bytes.fromhex('175a6f682303e313e7cae01f4579702ae6885644d46c15747c39b85e5a1fab667d2be070d383268d23a6387a4b3ec791')

def pohlig_hellman(g, h, p, factors):
    """Pohlig-Hellman algorithm for discrete log"""
    from sympy.ntheory.modular import crt
    
    remainders = []
    moduli = []
    
    for prime, exp in factors.items():
        q = prime ** exp
        print(f"  Solving for prime power {prime}^{exp} = {q}")
        
        # Reduce to subgroup of order q
        exp_val = (p - 1) // q
        g_q = pow(g, exp_val, p)
        h_q = pow(h, exp_val, p)
        
        print(f"    g^{exp_val} = {g_q}, h^{exp_val} = {h_q}")
        
        # Solve DLP in this subgroup
        if q == 2:
            # Trivial case
            if g_q == h_q:
                x_q = 0
            else:
                x_q = 1
        elif q < 2**25:  # Small enough for BSGS
            x_q = baby_step_giant_step(g_q, h_q, p, q)
        else:
            print(f"    Prime power too large, skipping")
            continue
        
        if x_q is not None:
            print(f"    Found: x ≡ {x_q} (mod {q})")
            remainders.append(x_q)
            moduli.append(q)
    
    if len(remainders) > 0:
        x_combined, mod_combined = crt(moduli, remainders)
        return x_combined, mod_combined
    return None, None

def baby_step_giant_step(g, h, p, order):
    """Baby-step giant-step algorithm"""
    import math
    m = int(math.ceil(math.sqrt(order))) + 1
    
    # Baby step
    table = {}
    g_power = 1
    for j in range(m):
        if g_power == h:
            return j
        table[g_power] = j
        g_power = (g_power * g) % p
    
    # Giant step
    g_inv_m = pow(g, -m, p)
    gamma = h
    for i in range(m):
        gamma = (gamma * g_inv_m) % p
        if gamma in table:
            return i * m + m + table[gamma]
    
    return None

print("Solving discrete logs using Pohlig-Hellman...")
all_remainders = []
all_moduli = []

for idx, (g, h, p) in enumerate(samples):
    print(f"\nSample #{idx+1}: p = {p}")
    
    # p-1 = 2 * q where q is prime
    factors = {2: 1, (p-1)//2: 1}
    
    x_combined, mod_combined = pohlig_hellman(g, h, p, factors)
    
    if x_combined is not None:
        print(f"  Combined result: key ≡ {x_combined} (mod {mod_combined})")
        
        # Verify
        if pow(g, x_combined, p) == h:
            print(f"  ✓ Verified!")
            all_remainders.append(x_combined)
            all_moduli.append(mod_combined)
        else:
            # Try adding the modulus
            for k in range(10):
                x_test = x_combined + k * mod_combined
                if pow(g, x_test, p) == h:
                    print(f"  ✓ Verified with k={k}!")
                    all_remainders.append(x_test)
                    all_moduli.append((p-1))
                    break

if len(all_remainders) > 0:
    print(f"\n{'='*60}")
    print(f"Combining {len(all_remainders)} results with CRT...")
    
    key_candidate, combined_mod = crt(all_moduli, all_remainders)
    print(f"Key candidate: {key_candidate}")
    print(f"Combined modulus: {combined_mod} ({combined_mod.bit_length()} bits)")
    print(f"Key candidate bit length: {key_candidate.bit_length()} bits")
    
    # Try different key lengths
    print(f"\nBrute forcing remaining bits...")
    for target_bytes in range(35, 50):
        target_bits = target_bytes * 8
        
        if target_bits < key_candidate.bit_length():
            continue
        
        if target_bits < combined_mod.bit_length():
            max_i = 1
        else:
            max_i = min(2 ** (target_bits - combined_mod.bit_length() + 3), 50000)
        
        found = False
        for i in range(max_i):
            key_int = key_candidate + i * combined_mod
            
            if key_int.bit_length() > target_bits:
                break
            
            try:
                key_bytes = long_to_bytes(key_int)
                if len(key_bytes) > target_bytes:
                    break
                key_bytes = long_to_bytes(key_int, target_bytes)
                
                cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
                pt = cipher.decrypt(ct)
                
                if b'0x' in pt or b'flag' in pt or b'{' in pt:
                    print(f"\n[+] FOUND FLAG!")
                    print(f"Key length: {target_bytes} bytes, i={i}")
                    print(f"Key: {key_int}")
                    try:
                        flag = unpad(pt, 16).decode()
                        print(f"Flag: {flag}")
                        found = True
                        exit(0)
                    except Exception as e:
                        print(f"Flag (raw): {pt}")
                        print(f"Error: {e}")
            except Exception as e:
                pass
        
        if max_i > 500 and target_bytes % 5 == 0:
            print(f"  Checked {target_bytes} bytes: {max_i} keys...")
    
    print("\nNo flag found :(")
else:
    print("\nCould not solve any discrete logs")
