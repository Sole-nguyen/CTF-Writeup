from Crypto.Util.number import *
from Crypto.Cipher import AES
import hashlib

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

# Try all samples to find the correct key
print("Trying all samples...")

for idx, (g, h, p) in enumerate(samples):
    print(f"\n{'='*60}")
    print(f"Sample #{idx+1}")
    print(f"Solving discrete log for p = {p} ({p.bit_length()} bits)")
    print(f"Finding x such that {g}^x ≡ {h} (mod {p})")
    
    q = (p - 1) // 2

# Try to solve discrete log using Pohlig-Hellman or baby-step giant-step
# Since key is bounded by the byte length, let's use discrete_log from sympy or implement BSGS

def baby_step_giant_step(g, h, p, order):
    """Baby-step giant-step algorithm for discrete log"""
    import math
    m = int(math.ceil(math.sqrt(order)))
    
    # Baby step: compute g^j for j = 0, 1, ..., m-1
    table = {}
    g_power = 1
    for j in range(m):
        if g_power == h:
            return j
        table[g_power] = j
        g_power = (g_power * g) % p
    
    # Giant step: compute h * g^(-mi) for i = 1, 2, ..., m
    g_inv_m = pow(g, -m, p)
    gamma = h
    for i in range(m):
        gamma = (gamma * g_inv_m) % p
        if gamma in table:
            return i * m + m + table[gamma]
    
    return None

    # Try to solve the discrete log
    key_int = baby_step_giant_step(g, h, p, q)
    if key_int is None:
        print("Trying with order p-1...")
        key_int = baby_step_giant_step(g, h, p, p-1)
    
    if key_int:
        print(f"Found discrete log: {key_int}")
        key_bytes = long_to_bytes(key_int)
        print(f"Key bytes: {key_bytes}")
        print(f"Key length: {len(key_bytes)}")
        
        # Try to decrypt with this key
        cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
        try:
            pt = cipher.decrypt(ct)
            if b'0xfun{' in pt:
                print(f"\n{'='*60}")
                print(f"[+] Found flag with sample #{idx+1}!")
                from Crypto.Util.Padding import unpad
                try:
                    pt_unpadded = unpad(pt, 16)
                    print(f"Flag: {pt_unpadded.decode()}")
                except:
                    print(f"Flag: {pt}")
                break
        except Exception as e:
            print(f"Decryption failed: {e}")
    else:
        print("Could not find discrete log")
