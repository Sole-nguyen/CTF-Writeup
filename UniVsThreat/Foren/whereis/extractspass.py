def extract_whitespace_password(filename):
    print(f"[*] Đang phân tích khoảng trắng từ {filename}...")
    try:
        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
    except Exception as e:
        print(f"[-] Lỗi đọc file: {e}")
        return

    # Lấy phần sau cùng của file (sau khi kết thúc khai báo code JS)
    if 'ping };' in content:
        ws_section = content.split('ping };')[1]
    else:
        ws_section = content

    # Lọc lấy Space, Tab và Non-breaking space (\xa0)
    ws_chars = [c for c in ws_section if c in [' ', '\t', '\xa0']]
    
    if not ws_chars:
        print("[-] Không tìm thấy khoảng trắng. Hãy đảm bảo dùng file empty.js gốc tải từ đề bài!")
        return

    # Kịch bản phổ biến: Space = 0, Tab = 1 (bỏ qua \xa0 hoặc xem nó là 0)
    mappings = [
        {' ': '0', '\t': '1', '\xa0': ''},  # Chỉ dùng Space và Tab
        {' ': '0', '\t': '1', '\xa0': '0'}  # Cả Space và \xa0 là 0
    ]

    for idx, mapping in enumerate(mappings):
        binary = "".join([mapping[c] for c in ws_chars if c in mapping and mapping[c] != ''])
        
        # Chuyển nhị phân -> ASCII
        text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
                
        # Lọc in ra chuỗi có chứa ký tự đọc được
        safe_text = "".join([c if 32 <= ord(c) <= 126 else '' for c in text])
        if len(safe_text) > 3:
            print(f"\n[+] Chuỗi mật khẩu tiềm năng (Kịch bản {idx+1}):")
            print(f"==> {safe_text}")

if __name__ == '__main__':
    extract_whitespace_password('empty.txt')