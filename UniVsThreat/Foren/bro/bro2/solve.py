import hashlib
import itertools
import string
import sys

# Hàm hỗ trợ đọc data từ file nhị phân
def read_file(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[-] Lỗi: Không tìm thấy file '{filename}'")
        sys.exit(1)

# TODO: Bạn cần đổi tên file dưới đây cho khớp với tên file thực tế 
# mà chương trình airlockauth đang đọc (có thể dùng lệnh `strings airlockauth` để tìm)
FILE1_PATH = 'file1.bin' 
FILE2_PATH = 'file2.bin'
FILE3_PATH = 'file3.bin'

def main():
    print("[*] Đang đọc dữ liệu từ các file...")
    file1_data = read_file(FILE1_PATH)
    file2_data = read_file(FILE2_PATH)
    file3_data = read_file(FILE3_PATH)

    # 1. Băm File 2 bằng SHA256
    hash2 = hashlib.sha256(file2_data).digest()

    # 2. Tính toán Target Prefix (4 bytes đầu tiên mà Final Hash bắt buộc phải có)
    # Công thức: Final_Hash[0..3] = File3[0..3] XOR "UVT{"
    magic_bytes = b"UVT{"
    target_prefix = bytes([file3_data[i] ^ magic_bytes[i] for i in range(4)])
    
    print(f"[*] Target prefix cần tìm (Hex): {target_prefix.hex()}")
    print("[*] Bắt đầu brute-force user_input...")

    # 3. Brute-force vét cạn user_input
    # Thường các challenge CTF sẽ giấu input là một chuỗi ngắn (tầm 1-6 ký tự)
    charset = string.ascii_letters + string.digits + string.punctuation
    found_input = None
    final_hash = None

    # Thử độ dài chuỗi từ 1 đến 6 (tăng lên nếu vẫn chưa tìm thấy)
    for length in range(1, 7):
        print(f"[*] Đang thử các chuỗi độ dài {length}...")
        for guess in itertools.product(charset, repeat=length):
            user_input = ''.join(guess).encode()
            
            # Khôi phục buffer: [32 bytes File 1] + [user_input] + [32 bytes SHA256(File 2)]
            payload = file1_data + user_input + hash2
            h = hashlib.sha256(payload).digest()
            
            # Kiểm tra 4 bytes đầu
            if h[:4] == target_prefix:
                found_input = user_input
                final_hash = h
                break
        if found_input:
            break

    # 4. Giải mã và in Flag
    if found_input:
        print(f"\n[+] SUCCESS! Tìm thấy user_input hợp lệ: {found_input.decode()}")
        print(f"[+] Final Hash (Key): {final_hash.hex()}")
        
        flag = bytearray()
        # Vòng lặp XOR từng byte của File 3 với Final Hash (lặp lại mỗi 32 bytes)
        for i in range(len(file3_data)):
            flag.append(file3_data[i] ^ final_hash[i % 32])
            
        print(f"\n[+] FLAG: {flag.decode(errors='ignore')}")
    else:
        print("\n[-] Không tìm thấy user_input. Bạn có thể cần tăng khoảng length hoặc kiểm tra lại nội dung các file.")

if __name__ == '__main__':
    main()