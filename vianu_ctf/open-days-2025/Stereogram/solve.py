import cv2
import numpy as np

img = cv2.imread('stereogram.png', 0).astype(float)
h, w = img.shape
P = 50 # Chu kỳ gốc
search_range = 10 # Tìm trong khoảng [P-10, P+10]

# Tạo một "chồng" các ảnh sai số (error layers)
diff_layers = []
for s in range(P - search_range, P + search_range + 1):
    shifted = np.roll(img, s, axis=1)
    # Dùng blur để so sánh theo cụm pixel (vùng lân cận) thay vì từng pixel lẻ
    diff = cv2.blur(np.abs(img - shifted), (5, 5))
    diff_layers.append(diff)

# Tại mỗi pixel, chọn giá trị dịch chuyển s làm sai số nhỏ nhất
depth_map_idx = np.argmin(np.stack(diff_layers), axis=0)
depth_map = (P - search_range) + depth_map_idx

# Chuẩn hóa để lưu thành ảnh
depth_map_final = cv2.normalize(depth_map.astype(np.uint8), None, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('depth_map_final.png', depth_map_final)