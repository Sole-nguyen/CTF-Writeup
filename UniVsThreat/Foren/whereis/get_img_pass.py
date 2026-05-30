from PIL import Image

def debug_image_password(img_path):
    print(f"[*] Đang quét LSB kênh Blue của {img_path}...")
    try:
        # Tắt warning bằng cách dùng get_flattened_data nếu có thể, hoặc bỏ qua
        img = Image.open(img_path).convert('RGB')
    except Exception as e:
        print(f"[-] Lỗi mở ảnh: {e}")
        return

    pixels = list(img.getdata())
    
    # Thử cả 3 vị trí bắt đầu (offset 0, 1, 2)
    for offset in range(3):
        binary = ""
        for i in range(offset, len(pixels), 3):
            b = pixels[i][2]  # Lấy kênh Blue
            binary += str(b & 1)
            
        # Thử 2 cách ghép bit: Bình thường và Đảo ngược (Little Endian)
        for reverse_bits in [False, True]:
            password = ""
            for i in range(0, len(binary), 8):
                byte_str = binary[i:i+8]
                if len(byte_str) == 8:
                    if reverse_bits:
                        byte_str = byte_str[::-1]
                    password += chr(int(byte_str, 2))
            
            # Chỉ lấy 50 ký tự đầu tiên để xem lướt
            preview = repr(password[:50])
            
            # Kiểm tra xem có vẻ giống chữ tiếng Anh/ASCII không (loại trừ trường hợp toàn \xff hoặc \x00)
            if "\\xff\\xff\\xff" not in preview and "\\x00\\x00\\x00" not in preview:
                print(f"\n[+] Offset {offset} | Đảo bit: {reverse_bits}")
                print(f"==> Dữ liệu thô: {preview}")

if __name__ == "__main__":
    debug_image_password('empty.png')