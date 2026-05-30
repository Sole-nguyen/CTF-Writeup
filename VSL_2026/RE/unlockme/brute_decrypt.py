from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import hashlib

raw_key_hex = "753a13ad4a45f9df5a7e92f220dcd647bc71a0e4"
ciphertext_hex = "ce49b6edd9ca1634525872f8289e576ab22efcf3cb3e02850c55a10a570b2afb9b968f82f8361eee3a5ab2ad6feba438d3b463f35bda45da3a4d8cf186ec4f3c"

ciphertext = binascii.unhexlify(ciphertext_hex)
raw_key_bytes = binascii.unhexlify(raw_key_hex)

# All possible key derivations
key_derivations = [
    ("MD5(hex_bytes)", hashlib.md5(raw_key_bytes).digest()),
    ("MD5(ascii_str)", hashlib.md5(raw_key_hex.encode()).digest()),
    ("SHA1(hex_bytes)[:16]", hashlib.sha1(raw_key_bytes).digest()[:16]),
    ("SHA1(ascii_str)[:16]", hashlib.sha1(raw_key_hex.encode()).digest()[:16]),
    ("SHA256(hex_bytes)[:16]", hashlib.sha256(raw_key_bytes).digest()[:16]),
    ("first_16_of_hex", raw_key_bytes[:16]),
]

# All possible IV strategies
iv_strategies = [
    ("zero", b'\x00' * 16, slice(None)),
    ("first_16_bytes", None, slice(16, None)),  # Will use ciphertext[:16] as IV
]

# All modes
modes = [
    ("CBC", AES.MODE_CBC),
    ("ECB", AES.MODE_ECB),
]

print("Searching for VSL{ flag...\n")

for key_name, key in key_derivations:
    for iv_name, iv_val, data_slice in iv_strategies:
        for mode_name, mode in modes:
            # Skip IV for ECB mode
            if mode == AES.MODE_ECB and iv_name != "zero":
                continue
            
            try:
                data = ciphertext[data_slice]
                
                if iv_name == "first_16_bytes" and mode == AES.MODE_CBC:
                    iv = ciphertext[:16]
                elif mode == AES.MODE_ECB:
                    cipher = AES.new(key, mode)
                    decrypted = cipher.decrypt(data)
                else:
                    iv = iv_val
                    cipher = AES.new(key, mode, iv)
                    decrypted = cipher.decrypt(data)
                
                if mode != AES.MODE_ECB or iv_name == "zero":
                    cipher = AES.new(key, mode, iv) if mode == AES.MODE_CBC else AES.new(key, mode)
                    decrypted = cipher.decrypt(data)
                
                # Try to decode
                try:
                    text = decrypted.decode('utf-8', errors='ignore')
                except:
                    continue
                
                # Check for flag
                if 'VSL{' in text:
                    print(f"🎉 FOUND!")
                    print(f"Key: {key_name}")
                    print(f"IV: {iv_name}")
                    print(f"Mode: {mode_name}")
                    print(f"FLAG: {text}")
                    print(f"Hex: {binascii.hexlify(decrypted).decode()}")
                    exit(0)
                    
            except Exception as e:
                pass

print("Flag not found with standard methods.")
print("\nTrying reverse engineering hints... checking for 'V' 'S' 'L' bytes separately")

# Check the decryption that gave us "VR9{"
key = hashlib.md5(raw_key_bytes).digest()
iv = ciphertext[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext[16:])

print(f"\nBest result decrypted bytes:")
for i in range(min(30, len(decrypted))):
    print(f"  {i:2d}: 0x{decrypted[i]:02x} {chr(decrypted[i]) if 32 <= decrypted[i] < 127 else '?'}")
