from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import hashlib

def get_flag_final():
    # Different key strategies
    raw_key_hex = "753a13ad4a45f9df5a7e92f220dcd647bc71a0e4"
    
    keys_to_try = [
        ("MD5(ASCII string)", hashlib.md5(raw_key_hex.encode('utf-8')).digest()),
        ("MD5(hex bytes)", hashlib.md5(binascii.unhexlify(raw_key_hex)).digest()),
        ("First 16 bytes of hex", binascii.unhexlify(raw_key_hex)[:16]),
        ("Last 16 bytes padded", binascii.unhexlify(raw_key_hex)[:16]),  # 20 bytes, take first 16
    ]
    
    # Ciphertext
    ciphertext_hex = "ce49b6edd9ca1634525872f8289e576ab22efcf3cb3e02850c55a10a570b2afb9b968f82f8361eee3a5ab2ad6feba438d3b463f35bda45da3a4d8cf186ec4f3c"
    ciphertext = binascii.unhexlify(ciphertext_hex)
    
    print(f"Total ciphertext length: {len(ciphertext)} bytes")
    print(f"Raw key length: {len(binascii.unhexlify(raw_key_hex))} bytes\n")
    
    # Try different IV strategies
    iv_strategies = [
        ("Zero IV", b'\x00' * 16, ciphertext),
        ("First 16 bytes as IV", ciphertext[:16], ciphertext[16:]),
    ]
    
    for key_name, key in keys_to_try:
        print(f"{'='*60}")
        print(f"Key: {key_name}")
        print(f"Key hex: {binascii.hexlify(key).decode()}")
        
        for iv_name, iv, data_to_decrypt in iv_strategies:
            print(f"\n  [{iv_name}]")
            
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_data = cipher.decrypt(data_to_decrypt)
                
                # Try with PKCS7 unpadding
                try:
                    unpadded = unpad(decrypted_data, AES.block_size)
                    result = unpadded.decode('utf-8', errors='ignore')
                except:
                    result = decrypted_data.decode('utf-8', errors='ignore')
                
                # Check for flag
                if 'VSL{' in result:
                    print(f"  🎉 FOUND THE FLAG: {result}")
                    return result
                else:
                    # Show first 40 chars
                    display = repr(result[:40])
                    print(f"  Result: {display}")
                
            except Exception as e:
                print(f"  Error: {e}")
    
    print("\nNo flag found!")

if __name__ == "__main__":
    get_flag_final()