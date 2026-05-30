from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

key_candidate = 31761140426186090673515719468712060583420693180899839323289392054876593910686738005570286201284813
combined_mod = 35480277790003719548667062934053316746447412615625066238286384765180116609817788905832466831862622

ct = bytes.fromhex('175a6f682303e313e7cae01f4579702ae6885644d46c15747c39b85e5a1fab667d2be070d383268d23a6387a4b3ec791')

# For a 42-byte (336-bit) key with 325-bit modulus, we have 2^11 = 2048 possibilities
# Try them all!

print("Searching for 42-byte key (2^11 = 2048 possibilities)...")

for i in range(2**12):  # Try a bit more just in case
    key_int = key_candidate + i * combined_mod
    
    # Must fit in 42 bytes
    if key_int.bit_length() > 336:
        break
    
    key_bytes = long_to_bytes(key_int, 42)
    
    try:
        cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
        pt = cipher.decrypt(ct)
        
        if b'0xfun{' in pt:
            print(f"\n[+] FOUND FLAG at i={i}!")
            print(f"Key length: 42 bytes")
            try:
                flag = unpad(pt, 16).decode()
                print(f"Flag: {flag}")
            except:
                print(f"Flag: {pt}")
            exit(0)
            
        if i % 500 == 0 and i > 0:
            print(f"Checked {i} keys...")
    except:
        pass

print("No flag found in 42-byte range")

# Maybe it's a different length? Try 40-45 bytes
print("\nTrying other byte lengths...")
for target_bytes in [40, 41, 43, 44, 45]:
    print(f"\nTrying {target_bytes} bytes...")
    target_bits = target_bytes * 8
    max_i = 2 ** (target_bits - combined_mod.bit_length() + 1) if target_bits > combined_mod.bit_length() else 100
    
    for i in range(min(max_i, 5000)):
        key_int = key_candidate + i * combined_mod
        
        if key_int.bit_length() > target_bits:
            break
        
        key_bytes = long_to_bytes(key_int, target_bytes)
        
        try:
            cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
            pt = cipher.decrypt(ct)
            
            if b'0xfun{' in pt:
                print(f"\n[+] FOUND FLAG!")
                print(f"Key length: {target_bytes} bytes, i={i}")
                try:
                    flag = unpad(pt, 16).decode()
                    print(f"Flag: {flag}")
                except:
                    print(f"Flag: {pt}")
                exit(0)
        except:
            pass

print("\nNo flag found :(")
