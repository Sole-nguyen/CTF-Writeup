from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Data from output.txt
iv = bytes.fromhex("ac518ee77848d87912548668d3240aa4")
enc = bytes.fromhex("ab425b6c2c0a6760a5e9c52ba25dfc47da97afeeceb9823e553dcccc971b0f25c876ea63ed867d77e3295082064a3f69")

# The secret key is provided in output.txt line 4
# We can extract it and use it to decrypt
# sk = (f, g, F, G)

# The encryption key is derived as: key = sha256(str(sk).encode()).digest()
# So we need to reconstruct the exact sk representation

# Read the sk from output.txt
with open("output.txt", "r") as f:
    lines = f.readlines()
    # Find the line with sk =
    for line in lines:
        if line.startswith("sk = "):
            sk_str = line.split(" = ", 1)[1].strip()
            print("[+] Found secret key in output.txt")
            
            # Hash it to get the AES key
            key = sha256(sk_str.encode()).digest()
            
            # Decrypt
            cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
            flag = unpad(cipher.decrypt(enc), 16)
            
            print(f"[+] FLAG: {flag.decode()}")
            break
