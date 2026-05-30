from pwn import *
import string
import sys

# Tắt log để đỡ rối mắt, chỉ hiện kết quả quan trọng
context.log_level = 'error'

# Charset bao gồm chữ, số và các ký tự đặc biệt thường gặp trong flag
charset = string.ascii_letters + string.digits + "{}_!"

flag = ""
binary_path = './medicine'

print(f"[*] Bắt đầu brute-force flag cho binary: {binary_path}")
print("[*] Alias: sol3_f1t | Mission: Medicine")

while True:
    found_char = False
    for char in charset:
        # Thử ghép ký tự hiện tại vào flag
        test_flag = flag + char
        
        try:
            # Khởi tạo process
            p = process(binary_path)
            
            # Gửi flag thử nghiệm + ký tự xuống dòng
            # Lưu ý: scanf %32s thường dừng ở khoảng trắng/newline
            p.sendline(test_flag.encode())
            
            # Đọc output. Nếu flag đúng một phần, chương trình sẽ chạy lâu hơn
            # hoặc không bị crash ngay lập tức tại bước kiểm tra ký tự đó.
            # Ta chờ xem process kết thúc với exit code nào.
            p.wait()
            
            exit_code = p.poll()
            
            # Phân tích Exit Code:
            # -11 (hoặc -SIGSEGV) thường là Segmentation Fault -> Flag SAI ở ký tự này (hoặc ký tự kế tiếp chưa có)
            # Tuy nhiên, logic bài này là: 
            # Nếu SAI -> Crash ngay. 
            # Nếu ĐÚNG -> Chạy tiếp để check ký tự sau -> Cần input tiếp -> EOF -> Có thể crash sau đó.
            
            # Mẹo: Với các bài dạng này, ký tự ĐÚNG thường KHÔNG gây ra crash TẠI VỊ TRÍ ĐÓ.
            # Nhưng vì chúng ta gửi thiếu độ dài (ví dụ gửi 1 ký tự trong khi cần 32),
            # chương trình có thể crash khi cố đọc ký tự tiếp theo.
            
            # Cách đơn giản nhất để debug script này là in ra exit code của một ký tự đúng (ví dụ thử format flag)
            # Giả sử flag bắt đầu bằng 'T' hoặc 'C' (CTF), hãy quan sát sự khác biệt.
            
            # UPDATE LOGIC DỰA TRÊN HINT:
            # "Segfault may occur if FLAG is incorrect"
            # => Ký tự SAI gây Crash (-11). Ký tự ĐÚNG sẽ giúp chương trình sống sót qua bước đó.
            
            if exit_code != -11: 
                flag += char
                print(f"[+] Found char: {char} | Current Flag: {flag}")
                found_char = True
                
                # Kiểm tra xem đã xong chưa (nếu output có chữ "Correct")
                output = p.recvall(timeout=0.1)
                if b"Correct" in output:
                    print(f"\n[SUCCESS] Flag found: {flag}")
                    sys.exit(0)
                
                break # Đã tìm thấy ký tự đúng cho vị trí này, break để tìm ký tự tiếp theo
            
            p.close()
            
        except Exception as e:
            print(f"Error: {e}")

    if not found_char:
        print("\n[-] Không tìm thấy ký tự tiếp theo. Có thể đã hết charset hoặc logic bị sai.")
        print(f"Last found: {flag}")
        break