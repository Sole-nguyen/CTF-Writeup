import string
import itertools

def fnv1a_32_9bytes(data):
    # Khởi tạo giá trị FNV offset basis (32-bit unsigned)
    h = 0x811c9dc5
    # Main gọi hàm với tham số 9, nghĩa là băm 9 ký tự đầu
    for i in range(9):
        # Thuật toán: i = 16777619 * (byte ^ i)
        h = h ^ data[i]
        h = (h * 16777619) & 0xffffffff
    return h

# Tập ký tự để thử (chữ cái và số)
chars = string.ascii_letters + string.digits

print("[*] Đang tìm payload thỏa mãn điều kiện (Hash % 1009 == 1)...")

# Thử các chuỗi ngắn để tìm kết quả nhanh nhất
for length in range(1, 10):
    for guess in itertools.product(chars, repeat=length):
        prefix = "".join(guess)
        # Bù cho đủ 9 ký tự (vì main truyền tham số 9)
        test_str = (prefix + "0" * 9)[:9]
        
        h = fnv1a_32_9bytes(test_str.encode())
        
        if h % 1009 == 1:
            # Tạo chuỗi 32 ký tự hoàn chỉnh (vì main check strlen == 32)
            payload = test_str + "A" * (32 - 9)
            print(f"\n[!] THÀNH CÔNG! Payload của bạn là: {payload}")
            print(f"[*] Hãy chạy: ./ragebait {payload}")
            exit()