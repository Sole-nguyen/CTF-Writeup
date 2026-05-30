from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

key_candidate = 31761140426186090673515719468712060583420693180899839323289392054876593910686738005570286201284813
combined_mod = 35480277790003719548667062934053316746447412615625066238286384765180116609817788905832466831862622

ct = bytes.fromhex('175a6f682303e313e7cae01f4579702ae6885644d46c15747c39b85e5a1fab667d2be070d383268d23a6387a4b3ec791')

print(f"Key candidate bit length: {Integer(key_candidate).nbits()}")
print(f"Combined modulus bit length: {Integer(combined_mod).nbits()}")

# Try different byte lengths
for target_bytes in [40, 41, 42, 43, 44, 45]:
    target_bits = target_bytes * 8
    bits_avail = target_bits - Integer(combined_mod).nbits()
    
    if bits_avail < 0:
        continue
        
    max_i = 2 ** bits_avail if bits_avail < 15 else 50000
    
    print(f"\n[*] Trying {target_bytes} bytes ({target_bits} bits), {bits_avail} bits free, max_i={max_i}")
    
    for i in range(max_i):
        key_int = int(key_candidate) + i * int(combined_mod)
        
        if Integer(key_int).nbits() > target_bits:
            break
        
        key_bytes = long_to_bytes(key_int)
        if len(key_bytes) > target_bytes:
            break
            
        # Pad to target length
        key_bytes = b'\x00' * (target_bytes - len(key_bytes)) + key_bytes
        
        cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
        pt = cipher.decrypt(ct)
        
        # Check all common flag formats
        for flag_format in [b'0xfun{', b'0xL4ugh{', b'flag{', b'FLAG{', b'CTF{', b'ctf{']:
            if flag_format in pt:
                print(f"\n[+] FOUND FLAG!")
                print(f"bytes={target_bytes}, i={i}")
                print(f"Key: {key_int}")
                try:
                    flag = unpad(pt, 16).decode()
                    print(f"Flag: {flag}")
                except:
                    print(f"Raw: {pt}")
                    try:
                        print(f"Decoded: {pt.decode(errors='ignore')}")
                    except:
                        pass
                exit(0)
        
        if max_i > 1000 and i > 0 and i % 5000 == 0:
            print(f"  Progress: {i}/{max_i}")

print("\nNo flag found :(")
