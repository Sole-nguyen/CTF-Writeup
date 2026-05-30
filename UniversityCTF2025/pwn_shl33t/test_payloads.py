#!/usr/bin/env python3
import socket
import time

# Connection details
host = "154.57.164.66"
port = 31072

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Receive the initial output
data = s.recv(4096)
print(data.decode())

# Try different payloads
payloads = [
    b'16',
    b'16\n',
    b'10',
    b'10\n',
    b'shl ebx, 16',
    b'shl ebx, 16\n',
]

for payload in payloads:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.recv(4096)  # initial banner
    print(f"\n--- Trying payload: {payload} ---")
    s.send(payload)
    time.sleep(0.5)
    try:
        response = s.recv(4096)
        print(response.decode())
    except:
        pass
    s.close()
