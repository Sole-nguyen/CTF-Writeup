import hashlib

# 1. Đọc file HTTP Payload đã xuất từ Wireshark
try:
    with open("send-chunks.php.bin", "rb") as f:
        content = f.read()
except FileNotFoundError:
    print("Vui lòng xuất file HTTP từ Wireshark và đặt tên là 'send-chunks.php.bin'")
    exit()

# 2. Tách các khối bằng chuỗi định dạng của server
parts = content.split(b"NXTCHNKHASH:")

blocks = []
all_next = set()

for p in parts:
    # Bỏ qua các chuỗi quá ngắn không hợp lệ
    if len(p) < 69: 
        continue
    
    # Lấy 64 bytes hash trỏ đến khối tiếp theo
    nxt = p[:64].decode('utf-8', errors='ignore')
    # Phần còn lại là dữ liệu thực (bỏ qua 5 byte chữ 'DATA:')
    data = p[69:]
    
    # Tính mã băm (SHA-256). Có thể server băm phần data hoặc toàn bộ khối
    h_data = hashlib.sha256(data).hexdigest()
    h_full = hashlib.sha256(b"NXTCHNKHASH:" + p).hexdigest()
    
    blocks.append({
        'next': nxt,
        'data': data,
        'h_data': h_data,
        'h_full': h_full
    })
    all_next.add(nxt)

# 3. Tạo từ điển để tra cứu nhanh các khối dữ liệu
hash_to_block = {}
for b in blocks:
    hash_to_block[b['h_data']] = b
    hash_to_block[b['h_full']] = b

# 4. Tìm khối khởi nguồn (Là khối không bị bất kỳ next_hash nào trỏ đến)
start_block = None
for b in blocks:
    if b['h_data'] not in all_next and b['h_full'] not in all_next:
        start_block = b
        break

if start_block:
    print("[+] Đã tìm thấy khối bắt đầu!")
else:
    print("[-] Không tìm thấy khối bắt đầu rõ ràng, sử dụng khối đầu tiên...")
    start_block = blocks[0]

# 5. Lần theo dâu vết "Next Hash" để khôi phục cấu trúc file
recovered = bytearray()
curr = start_block

while curr:
    recovered.extend(curr['data'])
    nxt_hash = curr['next']
    
    if nxt_hash == "0" * 64:
        print("[+] Đã nối đến khối dữ liệu cuối cùng.")
        break
        
    if nxt_hash in hash_to_block:
        curr = hash_to_block[nxt_hash]
    else:
        print("[-] Mất liên kết ở hash:", nxt_hash)
        break

# 6. Ghi dữ liệu đã khôi phục ra file SQL hoàn chỉnh
with open("recovered.sql", "wb") as f:
    f.write(recovered)

print("[+] Hoàn thành! Hãy kiểm tra file recovered.sql")