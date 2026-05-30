import re

with open('flag.ppm', 'rb') as f:
    data = f.read()

# Quét tìm tất cả các khối chứa CỰC NHIỀU khoảng trắng liên tiếp (ít nhất 30 ký tự)
matches = re.findall(b'[ \t\n\r\f]{30,}', data)

if not matches:
    print("[-] Không tìm thấy khối khoảng trắng nào!")
else:
    # Lấy khối khoảng trắng cuối cùng và dài nhất trong file
    hidden_data = matches[-1] 
    print(f"[*] Đã tìm thấy thành công khối khoảng trắng dài {len(hidden_data)} byte!\n")

    # Loại bỏ \r và \f để dọn rác, chỉ giữ lại Space (32), Tab (9), và Newline (10)
    mapping = {32: 'S', 9: 'T', 10: '\n', 13: '', 12: ''}
    visualized = "".join(mapping.get(b, '') for b in hidden_data)

    print("[*] Dạng trực quan (S = Khoảng trắng, T = Tab, N = Xuống dòng):")
    print(visualized[:200].replace('\n', 'N') + "...\n")

    # Tình huống 1: Nhị phân (Space = 0, Tab = 1)
    binary_1 = visualized.replace('\n', '').replace('S', '0').replace('T', '1')
    if len(binary_1) >= 8:
        try:
            chars = [chr(int(binary_1[i:i+8], 2)) for i in range(0, len(binary_1)-len(binary_1)%8, 8)]
            print("[*] Thử giải mã Nhị phân (S=0, T=1):", "".join(chars))
        except: pass

    # Tình huống 2: Nhị phân (Space = 1, Tab = 0)
    binary_2 = visualized.replace('\n', '').replace('S', '1').replace('T', '0')
    if len(binary_2) >= 8:
        try:
            chars = [chr(int(binary_2[i:i+8], 2)) for i in range(0, len(binary_2)-len(binary_2)%8, 8)]
            print("[*] Thử giải mã Nhị phân (S=1, T=0):", "".join(chars))
        except: pass
