import os

def solve_ghost_compiler(file_path):
    if not os.path.exists(file_path):
        print(f"[-] Không tìm thấy file {file_path}.")
        return

    with open(file_path, 'rb') as f:
        data = bytearray(f.read())

    file_size = len(data)
    print(f"[*] Đang phân tích file {file_path} (Kích thước: {file_size} bytes)...")

    # Kiểm tra dấu hiệu file đã bị wipe (64 bytes 0x00 liên tiếp)
    if b'\x00' * 64 in data:
        print("\n[!] CẢNH BÁO ĐỎ (ノಠ_ಠ)ノ: Tìm thấy block 64-byte 0x00.")
        print("[!] File này 100% ĐÃ BỊ CHẠY và tự ghi đè mất cờ!")
        print("[!] Vui lòng xóa file này, giải nén lại một file mới tinh từ file ZIP của BTC và thử lại.")

    print("\n[*] Đang brute-force tìm offset (Quá trình này có thể mất 10-15 giây, đi pha tách trà nhé)...")
    
    # Mở rộng range thêm 1 index đề phòng flag nằm ở sát cuối file
    for offset in range(file_size - 63):
        key = 0xCBF29CE484222325
        
        # Bước 1: Tính FNV-1a hash (bỏ qua 64 byte flag)
        for i in range(file_size):
            if offset <= i < offset + 64:
                continue
            key ^= data[i]
            key = (key * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
            
        key ^= 0xCAFEBABE00000000

        # Bước 2: Thử giải mã 8 byte đầu để check signature
        temp_key = key
        decrypted = bytearray()
        for i in range(8):
            c = data[offset + i]
            p = c ^ (temp_key & 0xFF)
            decrypted.append(p)
            temp_key = ((temp_key >> 1) | ((temp_key & 1) << 63)) & 0xFFFFFFFFFFFFFFFF

        if decrypted == b"BITSCTF{":
            print(f"\n[+] BINGO! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Tìm thấy encrypted flag tại offset: {hex(offset)}")
            
            # Bước 3: Giải mã toàn bộ 64 byte
            flag = bytearray()
            temp_key = key
            for i in range(64):
                c = data[offset + i]
                p = c ^ (temp_key & 0xFF)
                flag.append(p)
                temp_key = ((temp_key >> 1) | ((temp_key & 1) << 63)) & 0xFFFFFFFFFFFFFFFF
                
            print(f"[+] Flag: {flag.decode('utf-8', errors='ignore').strip(chr(0))}")
            return

    print("\n[-] Vẫn không tìm thấy flag. Xác nhận file này không chứa Ciphertext gốc.")
    print("[*] Cách khắc phục: Xóa file hiện tại -> Giải nén lại file zip -> CHẠY THẲNG SCRIPT NÀY lên file mới giải nén.")

solve_ghost_compiler("ghost_compiler")