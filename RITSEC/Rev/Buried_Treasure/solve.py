def rc4_decrypt(data, key):
    S = list(range(256))
    j = 0
    # Khởi tạo S-box (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Giải mã dữ liệu (PRGA)
    res = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        res.append(byte ^ S[(S[i] + S[j]) % 256])
    return res

# Đọc file layer 3
with open('layer3_binary', 'rb') as f:
    raw = f.read()

# Key nằm tại offset 0x240 (16 bytes): "@GVg S*Hr c;S< K"
key = raw[0x240 : 0x240+16]
# Dữ liệu mã hóa bắt đầu tại offset 0x485 với size 0x512F8
data_offset = 0x485
size = 0x512F8
encrypted_data = raw[data_offset : data_offset + size]

decrypted = rc4_decrypt(encrypted_data, key)

with open('real_final_binary', 'wb') as f:
    f.write(decrypted)

print("[+] Đã trích xuất file 'real_final_binary' thành công!")