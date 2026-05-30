def rc4_decrypt(data, key):
    S = list(range(256))
    j = 0
    # KSA (Key-Scheduling Algorithm)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # PRGA (Pseudo-Random Generation Algorithm)
    res = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        res.append(byte ^ S[(S[i] + S[j]) % 256])
    return res

# Đọc layer3_binary
with open('layer3_binary', 'rb') as f:
    raw = f.read()

# Lấy Key tại offset tương ứng với VA 0x200240 (thường là 0x240)
key = raw[0x240:0x240+16]
# Lấy Encrypted Data tại offset tương ứng với VA 0x25177D
# Bạn cần kiểm tra File Offset của 0x25177D trong IDA nhé!
# Giả sử offset là 0x5177D (tùy thuộc vào cách IDA load)
data_offset = 0x5177D 
size = 0x512F8
encrypted_data = raw[data_offset : data_offset + size]

decrypted_final = rc4_decrypt(encrypted_data, key)

with open('final_treasure.txt', 'wb') as f:
    f.write(decrypted_final)

print("[+] Đã giải mã xong lõi RC4! Kiểm tra file 'final_treasure.txt'")
