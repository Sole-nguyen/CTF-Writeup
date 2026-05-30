import pwn
from sage.all import *
import sys

# --- Configuration ---
# NIST P-256 (secp256r1) parameters
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

pwn.context.log_level = 'info'

def get_smart_curve(start_b):
    """
    Tìm đường cong lỗi có order 'mịn' (smooth) để tấn công Pohlig-Hellman.
    Đã tối ưu để không bị treo khi gặp số khó.
    """
    b_prime = start_b
    # Tạo sẵn danh sách số nguyên tố nhỏ để lọc nhanh
    small_primes = list(primes(1000))
    
    pwn.log.info(f"Searching for smooth curve starting from b_offset...")
    
    count = 0
    while True:
        b_prime += 1
        count += 1
        
        # In dấu chấm mỗi 100 lần thử để biết script đang chạy
        if count % 100 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()

        try:
            # Tạo đường cong trên trường hữu hạn
            E = EllipticCurve(GF(p), [a, b_prime])
            order = E.order()
            
            # --- TỐI ƯU HÓA (QUICK FILTER) ---
            # Thay vì gọi factor() ngay, ta chia thử cho các số nhỏ trước.
            temp_order = order
            for sp in small_primes:
                while temp_order % sp == 0:
                    temp_order //= sp
            
            # Nếu phần còn lại vẫn quá lớn (> 45 bit), nghĩa là chứa thừa số nguyên tố to.
            # Việc giải DLP sẽ rất lâu -> BỎ QUA NGAY.
            if temp_order > 2**45:
                continue
            # ---------------------------------

            # Nếu qua được bước trên nghĩa là order rất đẹp, in ra và trả về
            sys.stdout.write("\n")
            return E, order
            
        except Exception:
            continue

def parse_point(s):
    s = s.strip()
    if b"Point" not in s:
        return None
    inner = s.split(b'(')[1].split(b')')[0]
    x_str, y_str = inner.split(b',')
    return int(x_str), int(y_str)

def solve():
    r = pwn.remote('challenges.ctf.sd', 33725)
    
    crt_remainders = []
    crt_moduli = []
    
    # Bắt đầu tìm từ b + một khoảng nào đó để tránh trùng lặp
    current_b_search = b + 100 
    
    for i in range(5):
        pwn.log.info(f"--- Query {i+1}/5 ---")
        
        # Tìm đường cong lỗi
        E_bad, order_bad = get_smart_curve(current_b_search)
        
        # Cập nhật vị trí tìm kiếm cho lần sau để không tìm lại đường cong cũ
        current_b_search = E_bad.a4() + 200
        
        pwn.log.success(f"Found invalid curve! Order factors: {factor(order_bad)}")
        
        # Chọn điểm P để gửi
        P = E_bad.gen(0)
        # Tránh điểm vô cực
        if P == E_bad(0):
            P = E_bad.gen(0) * 2

        # Gửi C1
        r.recvuntil(b'Input C1 >')
        r.sendline(f"Point({P[0]}, {P[1]})".encode())
        
        # Gửi C2 (Chọn C2 = P để đơn giản hóa phương trình)
        r.recvuntil(b'Input C2 >', timeout=2)
        r.sendline(f"Point({P[0]}, {P[1]})".encode())
        
        # Nhận kết quả S
        response = r.recvline()
        if b"Point" not in response:
            response = r.recvline()
            
        sx, sy = parse_point(response)
        pwn.log.info(f"Received S: ({sx}, {sy})")
        
        # Đưa S về đường cong lỗi để tính toán
        try:
            S = E_bad(sx, sy)
        except TypeError:
            pwn.log.error("Point S not on curve. Something is wrong.")
            return

        # Giải bài toán Logarit rời rạc (DLP)
        # S = (1 - d) * P  => k = 1 - d
        # Vì order nhỏ (smooth), hàm discrete_log của Sage sẽ chạy rất nhanh
        k = discrete_log(S, P, operation='+')
        d_mod = (1 - k) % order_bad
        
        pwn.log.info(f"Partial d recovered: {d_mod} (mod {order_bad})")
        
        crt_remainders.append(d_mod)
        crt_moduli.append(order_bad)
        
        # Kiểm tra xem đã đủ dữ kiện để khôi phục d chưa
        if prod(crt_moduli) > 2**256:
            pwn.log.success("Collected enough moduli!")
            break

    pwn.log.info("Reconstructing d using CRT...")
    d = crt(crt_remainders, crt_moduli)
    
    pwn.log.success(f"Recovered secret key d: {d}")
    print(f"Decimal: {d}")
    print(f"Hex: {hex(d)}")

if __name__ == "__main__":
    solve()