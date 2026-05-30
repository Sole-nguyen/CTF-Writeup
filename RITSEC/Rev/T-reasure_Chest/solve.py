import struct

def decrypt(v, k):
    v0, v1 = struct.unpack("<II", v)
    k0, k1, k2, k3 = k
    delta = 0x9E3779B9
    sum_val = (delta * 32) & 0xffffffff
    
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum_val) ^ ((v0 >> 5) + k3))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum_val) ^ ((v1 >> 5) + k1))) & 0xffffffff
        sum_val = (sum_val - delta) & 0xffffffff
        
    return struct.pack("<II", v0, v1)

# Key trích xuất từ Assembly
key_str = b"tiny_encrypt_key"
key = struct.unpack("<IIII", key_str)

# Ciphertext từ địa chỉ 0x404080 (padded to 40 bytes)
ciphertext = bytes.fromhex("38755BCB44D2BE5D969C5643EA9806754A4813E6D4E88E4F72708BFFDC99F876C5C9000000000000")

result = b""
for i in range(0, len(ciphertext), 8):
    block = ciphertext[i:i+8]
    if len(block) == 8:
        result += decrypt(block, key)

print("Magic Word là:", result[:34].decode('ascii', errors='ignore'))
