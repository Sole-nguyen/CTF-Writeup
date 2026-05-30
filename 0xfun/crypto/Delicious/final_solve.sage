from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

key_candidate = 31761140426186090673515719468712060583420693180899839323289392054876593910686738005570286201284813
combined_mod = 4541475557120476102229384055558824543545268814800008478500657249943054926056676979946555754478415616

ct = bytes.fromhex('175a6f682303e313e7cae01f4579702ae6885644d46c15747c39b85e5a1fab667d2be070d383268d23a6387a4b3ec791')

print(f"Key candidate: {key_candidate}")
print(f"Combined modulus: {combined_mod} ({Integer(combined_mod).nbits()} bits)")
print(f"Key candidate bit length: {Integer(key_candidate).nbits()} bits")

# Try all reasonable key lengths more exhaustively
print("\nSearching for flag...")
for target_bytes in range(30, 55):
    target_bits = target_bytes * 8
    
    # Calculate how many iterations to try
    if target_bits < Integer(key_candidate).nbits():
        continue
    
    if target_bits < Integer(combined_mod).nbits():
        max_i = 2
    else:
        bits_remaining = target_bits - Integer(combined_mod).nbits()
        max_i = min(2 ** bits_remaining, 1000000)
    
    if max_i < 2:
        continue
        
    print(f"\nTrying {target_bytes} bytes ({target_bits} bits), max_i={max_i}")
    
    for i in range(max_i):
        key_int = int(key_candidate) + i * int(combined_mod)
        
        if Integer(key_int).nbits() > target_bits:
            break
        
        try:
            key_bytes = long_to_bytes(key_int)
            if len(key_bytes) > target_bytes:
                break
            
            # Pad to target length
            key_bytes = b'\x00' * (target_bytes - len(key_bytes)) + key_bytes
            
            cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
            pt = cipher.decrypt(ct)
            
            # Check for any printable content
            if all(32 <= b < 127 or b in [9, 10, 13] for b in pt[:20]):
                print(f"\n[*] Found printable content at bytes={target_bytes}, i={i}")
                print(f"Key: {key_int}")
                print(f"Plaintext: {pt}")
                
            # Check for flag
            if b'0xfun{' in pt or b'0xL4ugh{' in pt or b'flag{' in pt:
                print(f"\n[+] FOUND FLAG!")
                print(f"Key length: {target_bytes} bytes, i={i}")
                print(f"Key: {key_int}")
                try:
                    flag = unpad(pt, 16).decode()
                    print(f"Flag: {flag}")
                except Exception as e:
                    print(f"Flag (raw): {pt}")
                    try:
                        print(f"Flag (decoded): {pt.decode()}")
                    except:
                        pass
                exit(0)
        except Exception as e:
            pass
        
        if max_i > 1000 and i > 0 and i % 10000 == 0:
            print(f"  Progress: {i}/{max_i} checked...")

print("\nNo flag found :(")
