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

# Try the key_candidate directly with its natural byte length
print("\nTrying key candidate with natural byte length...")
for i in range(100):
    key_int = int(key_candidate) + i * int(combined_mod)
    key_bytes = long_to_bytes(key_int)
    
    print(f"\ni={i}: Key has {len(key_bytes)} bytes")
    
    try:
        cipher = AES.new(hashlib.sha256(key_bytes).digest(), AES.MODE_ECB)
        pt = cipher.decrypt(ct)
        
        # Print first 20 bytes in hex and as string
        print(f"  First 20 bytes (hex): {pt[:20].hex()}")
        print(f"  First 20 bytes (repr): {repr(pt[:20])}")
        
        # Check for flag
        if b'0xfun{' in pt or b'0xL4ugh{' in pt or b'flag{' in pt or b'CTF{' in pt:
            print(f"\n[+] FOUND FLAG!")
            print(f"Key: {key_int}")
            try:
                flag = unpad(pt, 16).decode()
                print(f"Flag: {flag}")
                exit(0)
            except Exception as e:
                print(f"Flag (raw): {pt}")
                try:
                    # Try different unpadding strategies
                    for pad_len in range(1, 17):
                        if pt[-pad_len:] == bytes([pad_len]) * pad_len:
                            flag = pt[:-pad_len].decode()
                            print(f"Flag (manual unpad): {flag}")
                            exit(0)
                except:
                    pass
    except Exception as e:
        print(f"  Error: {e}")

print("\nNo flag found :(")
