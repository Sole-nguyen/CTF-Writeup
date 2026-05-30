import zlib
from itertools import cycle

# Input ban đầu
bytes_a = b'k\x00@\x003\x00@\x00y\x00@\x00!\x00@\x00'
bytes_b = b'\x13\xaf\x8a)\x1a\x99\x0f\xefZ\x1b4\x88\xe7DO\tY\xbdv\x13E\x00W\x0b]}\xd0$k^[)\xe3\x00\x00\x00'

# 1. Tái tạo Key
key = bytes_a[::4] # b'k3y!'

# 2. XOR Decrypt (để lấy Zlib stream)
xor_decrypted = bytes([b ^ k for b, k in zip(bytes_b, cycle(key))])
print(f"[*] XOR Decrypted (Hex): {xor_decrypted.hex()[:10]}...") 
# Mong đợi bắt đầu bằng 789c...

# 3. Zlib Decompress
try:
    # zlib.decompress sẽ tự động dừng khi hết stream hợp lệ, bỏ qua rác phía sau (nếu có)
    flag = zlib.decompress(xor_decrypted)
    print(f"\n>>>>> FLAG FOUND: {flag.decode('utf-8', errors='ignore')} <<<<<")
except Exception as e:
    print(f"[!] Lỗi giải nén: {e}")