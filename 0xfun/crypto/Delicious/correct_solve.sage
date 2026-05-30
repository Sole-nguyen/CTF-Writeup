from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

key_candidate = 31761140426186090673515719468712060583420693180899839323289392054876593910686738005570286201284813
combined_mod = 35480277790003719548667062934053316746447412615625066238286384765180116609817788905832466831862622

ct = bytes.fromhex('175a6f682303e313e7cae01f4579702ae6885644d46c15747c39b85e5a1fab667d2be070d383268d23a6387a4b3ec791')

print(f"Key candidate: {key_candidate}")
print(f"Combined modulus: {combined_mod}")
print(f"Bit lengths: key={Integer(key_candidate).nbits()}, mod={Integer(combined_mod).nbits()}")

# Try 42 bytes (336 bits) - we have 11 bits of freedom
print("\nTrying 42-byte keys (2^11 = 2048 possibilities)...")
for i in range(2**11 + 100):  # Try a bit more
    key_int = int(key_candidate) + i * int(combined_mod)
    
    if Integer(key_int).nbits() > 336:
        print(f"Stopped at i={i}, key would be too large")
        break
    
    key_bytes = long_to_bytes(key_int, 42)
    
    try:
        cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
        pt = cipher.decrypt(ct)
        
        # Check for flag formats
        if b'0xfun{' in pt or b'0xL4ugh{' in pt or b'flag{' in pt:
            print(f"\n[+] FOUND FLAG!")
            print(f"i={i}")
            print(f"Key: {key_int}")
            try:
                flag = unpad(pt, 16).decode()
                print(f"Flag: {flag}")
            except Exception as e:
                print(f"Raw: {pt}")
                try:
                    print(f"Decoded: {pt.decode(errors='ignore')}")
                except:
                    pass
            exit(0)
            
        if i % 200 == 0:
            print(f"Checked {i}...")
    except Exception as e:
        pass

print("\nNo flag found :(")
