import sys

# Cấu hình
sys.setrecursionlimit(2000)

# Dữ liệu bạn đã tìm được
p = 104191972189504036777696166231349461684316162238681731929158295674591930643730993528824336997235266091139256745204645368709924156944545641280200567743838559790441947310990502632677158859502017500820944362902197067105853457051639857660906995746784454935073835527809617894339685442179858460325916483129729156351
q = 111117688295539631073406868857672578062109978805027636729899551779303151567988708945737603186246921190225155540144830265413472023272557443502565095519273404605975722508819932376310203301497462457441141904481630861798582419619886582843270765745615848859707117184787103813443688565955586368641270763388999292747
c = 4076499216416562896607441161849625990047067800665233407329196341540304308648851286217843088574720496112040934416510938682846567006808806010955921894978744639999560939385998309826612716572297961147343647566989002739744629380117872478800844703421167539558650736951573012109179090419063845190127599968982469602914208703636984004199567214853971463422671349587993404007992477629764085581293548006892140104708828058826600334161006488685079586296737011303994925944419846262719619542090760222527573288314177260270227503471544970415885712109366649795000097050560179546478161308265772556681319650087987273824051482087965825610

n = p * q
phi = (p - 1) * (q - 1)
e = p ^ q

# 1. Xử lý GCD = 4
# Ta có m^e = c (mod n)
# e chia hết cho 4, đặt e = 4 * e_prime
# => (m^e_prime)^4 = c (mod n)
# Chiến thuật: 
#   B1: Tìm x sao cho x^4 = c (mod n)
#   B2: Giải m^e_prime = x => m = x^d_prime (với d_prime là nghịch đảo của e_prime)

g = 4
e_prime = e // g
d_prime = pow(e_prime, -1, phi)

# 2. Hàm tìm căn bậc 4 mod P
# Áp dụng cho số nguyên tố P chia 4 dư 3 (Blum integer), cả p và q bài này đều thỏa mãn.
def get_4th_roots(val, P):
    # Vì P = 3 mod 4:
    # Căn bậc 2 của a là a^((P+1)/4)
    
    # Bước 1: Tìm căn bậc 2 đầu tiên: z^2 = val mod P
    exp = (P + 1) // 4
    z1 = pow(val, exp, P)
    
    # z1 hoặc -z1 phải là thặng dư bậc hai (Quadratic Residue - QR) để khai căn tiếp được.
    # Kiểm tra Euler criterion: z^((P-1)/2) == 1
    if pow(z1, (P - 1) // 2, P) == 1:
        z = z1
    else:
        z = P - z1  # Lấy -z1
        
    # Bước 2: Tìm căn bậc 2 tiếp theo: x^2 = z mod P
    x = pow(z, exp, P)
    
    # Nghiệm là x và -x
    return [x, P - x]

# Tìm nghiệm trên từng trường nguyên tố
rp = get_4th_roots(c, p)
rq = get_4th_roots(c, q)

# 3. Kết hợp nghiệm bằng CRT (Chinese Remainder Theorem)
# Dùng pow(a, -1, b) của Python để tính nghịch đảo
q_inv = pow(q, -1, p)
p_inv = pow(p, -1, q)

print("[*] Dang thu cac nghiem...")
found = False

for u in rp:
    for v in rq:
        # CRT: x = u*q*q_inv + v*p*p_inv (mod n)
        x = (u * q * q_inv + v * p * p_inv) % n
        
        # Lúc này x là một ứng cử viên cho m^(e_prime)
        # Ta giải mã nốt phần mũ e_prime: m = x^d_prime
        m = pow(x, d_prime, n)
        
        try:
            # Chuyển số nguyên m sang bytes (thay thế long_to_bytes)
            # Tính số byte cần thiết: (bit_length + 7) // 8
            flag_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
            
            # Kiểm tra format flag
            if b"TSGCTF" in flag_bytes:
                print(f"[+] Flag found: {flag_bytes.decode()}")
                found = True
                break
        except Exception:
            continue
    if found:
        break

if not found:
    print("[-] Khong tim thay flag trong cac nghiem.")