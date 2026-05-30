from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
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

print("Solving discrete logs using SageMath...")
all_remainders = []
all_moduli = []

for idx, (g, h, p) in enumerate(samples):
    print(f"\nSample #{idx+1}: p = {p} ({Integer(p).nbits()} bits)")
    
    try:
        # Use SageMath's built-in discrete_log
        F = GF(p)
        g_elem = F(g)
        h_elem = F(h)
        
        print(f"  Solving discrete log...")
        x = discrete_log(h_elem, g_elem)
        print(f"  Found: key ≡ {x} (mod {p-1})")
        
        # Verify
        if pow(int(g), int(x), int(p)) == int(h):
            print(f"  ✓ Verified!")
            all_remainders.append(int(x))
            all_moduli.append(int(p-1))
        else:
            print(f"  ✗ Verification failed!")
    except Exception as e:
        print(f"  Failed: {e}")

if len(all_remainders) > 0:
    print(f"\n{'='*60}")
    print(f"Combining {len(all_remainders)} results with CRT...")
    
    # Use CRT to combine
    key_candidate = crt(all_remainders, all_moduli)
    combined_mod = prod(all_moduli)
    
    print(f"Key candidate: {key_candidate}")
    print(f"Combined modulus: {combined_mod} ({Integer(combined_mod).nbits()} bits)")
    print(f"Key candidate bit length: {Integer(key_candidate).nbits()} bits")
    
    # Try different key lengths
    print(f"\nBrute forcing remaining bits...")
    for target_bytes in range(35, 50):
        target_bits = target_bytes * 8
        
        if target_bits < Integer(key_candidate).nbits():
            continue
        
        combined_bits = Integer(combined_mod).nbits()
        if target_bits < combined_bits:
            max_i = 1
        else:
            max_i = min(2 ** (target_bits - combined_bits + 3), 50000)
        
        for i in range(max_i):
            key_int = int(key_candidate) + i * int(combined_mod)
            
            if Integer(key_int).nbits() > target_bits:
                break
            
            try:
                key_bytes = long_to_bytes(key_int)
                if len(key_bytes) > target_bytes:
                    break
                key_bytes = long_to_bytes(key_int, target_bytes)
                
                cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
                pt = cipher.decrypt(ct)
                
                # Check for flag format
                if b'0xfun{' in pt or b'0xL4ugh{' in pt:
                    print(f"\n[+] FOUND FLAG!")
                    print(f"Key length: {target_bytes} bytes, i={i}")
                    print(f"Key: {key_int}")
                    try:
                        flag = unpad(pt, 16).decode()
                        print(f"Flag: {flag}")
                        exit(0)
                    except Exception as e:
                        print(f"Flag (raw): {pt}")
                        # Try without unpadding
                        try:
                            print(f"Flag (decoded): {pt.decode()}")
                        except:
                            pass
                        exit(0)
            except Exception as e:
                pass
        
        if max_i > 500 and target_bytes % 5 == 0:
            print(f"  Checked {target_bytes} bytes: {max_i} keys...")
    
    print("\nNo flag found :(")
else:
    print("\nCould not solve any discrete logs")
