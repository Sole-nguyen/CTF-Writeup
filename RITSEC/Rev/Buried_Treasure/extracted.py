import os

def unpack_layer(filename, layer_num):
    with open(filename, 'rb') as f:
        data = f.read()

    # Vẫn sử dụng các offset đã xác định
    key_offset = 0x240
    data_offset = 0x465
    
    # Kích thước payload thường nằm ở 0x556C0 hoặc tương đương
    # Ở lớp này là 349888 bytes
    size = 0x556C0 
    
    key = data[key_offset : key_offset + 16]
    encrypted_blob = data[data_offset : data_offset + size]
    
    if len(encrypted_blob) < size:
        print(f"[-] Layer {layer_num} is too small, possibly the end.")
        return None

    decrypted = bytearray()
    for i in range(len(encrypted_blob)):
        decrypted.append(encrypted_blob[i] ^ key[i % 16])
        
    next_file = f"layer{layer_num + 1}_binary"
    with open(next_file, 'wb') as f:
        f.write(decrypted)
        
    print(f"[+] Layer {layer_num} extracted to {next_file} (Size: {len(decrypted)})")
    
    # Kiểm tra xem có Flag trong lớp vừa trích xuất không
    if b"RITSEC{" in decrypted:
        print(f"[!!!] FLAG FOUND in {next_file}!")
        # In flag ra (giả sử flag kết thúc bằng '}')
        start = decrypted.find(b"RITSEC{")
        end = decrypted.find(b"}", start)
        print(f"Flag: {decrypted[start:end+1].decode()}")
        return "FOUND"
        
    return next_file

# Chạy vòng lặp tự động bắt đầu từ layer3_binary
current_file = 'layer3_binary'
for i in range(3, 100): # Thử tối đa 100 lớp
    result = unpack_layer(current_file, i)
    if result == "FOUND":
        break
    if result is None:
        print("[-] Stopped unpacking.")
        break
    current_file = result