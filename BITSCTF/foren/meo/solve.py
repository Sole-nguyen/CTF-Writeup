import numpy as np
from PIL import Image

def arnold_cat_map_forward(img_matrix, style, iterations):
    """
    Hàm chạy TỚI thuật toán Arnold's Cat Map.
    Style = a = b.
    """
    a = style
    b = style
    N = img_matrix.shape[0]
    curr_img = img_matrix.copy()
    
    for _ in range(iterations):
        new_img = np.zeros_like(curr_img)
        for x in range(N):
            for y in range(N):
                # Công thức chuẩn Arnold's Cat Map (Forward)
                nx = (x + a * y) % N
                ny = (b * x + (a * b + 1) * y) % N
                
                # Áp dụng pixel vào vị trí mới
                new_img[nx, ny] = curr_img[x, y]
        curr_img = new_img
        
    return curr_img

def main():
    img_path = "transmission.png"
    
    try:
        # Load lại file ảnh gốc truyền vào
        img = Image.open(img_path).convert("L")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{img_path}'.")
        return
        
    data = np.array(img)
    print("Bắt đầu giải mã bằng phương pháp Hoàn thành Chu kỳ (Period Completion)...")
    
    # 1. Giải mã Stage 3 (Cần 67 vòng nữa để hoàn thành chu kỳ 96)
    print("Đang xử lý Stage 3 (Style 1, chạy tiếp 67 vòng)...")
    data = arnold_cat_map_forward(data, style=1, iterations=67)
    
    # 2. Giải mã Stage 2 (Cần 27 vòng nữa để hoàn thành chu kỳ 64)
    print("Đang xử lý Stage 2 (Style 2, chạy tiếp 27 vòng)...")
    data = arnold_cat_map_forward(data, style=2, iterations=27)
    
    # 3. Giải mã Stage 1 (Cần 49 vòng nữa để hoàn thành chu kỳ 96)
    print("Đang xử lý Stage 1 (Style 1, chạy tiếp 49 vòng)...")
    data = arnold_cat_map_forward(data, style=1, iterations=49)
    
    # Lưu kết quả
    output_path = "flag_revealed_v2.png"
    result_img = Image.fromarray(data)
    result_img.save(output_path)
    
    print(f"\n[+] Đã xong! Hãy mở file '{output_path}' để kiểm tra lại nhé.")

if __name__ == "__main__":
    main()