#!/usr/bin/env python3
"""
Simple test: Just connect and read everything server sends
Maybe flag is in banner/prompt?
"""
import socket
import time

print("[*] Test 1: Read initial banner...")
s = socket.socket()
s.settimeout(10)
s.connect(('34.84.25.24', 58554))

# Read everything without sending anything
time.sleep(2)
try:
    data = s.recv(8192)
    print(f"Initial data ({len(data)} bytes):")
    print(data)
    print(data.decode(errors='ignore'))
except:
    pass
s.close()

print("\n" + "="*60)
print("[*] Test 2: Send invalid input and check error...")
s = socket.socket()
s.settimeout(10)
s.connect(('34.84.25.24', 58554))

s.recv(4096)
s.sendall(b"invalid\n")
time.sleep(1)

try:
    data = s.recv(8192)
    print(f"Error response ({len(data)} bytes):")
    print(data.decode(errors='ignore'))
    
    if b'TSGCTF{' in data:
        print("\n[+] FLAG IN ERROR MESSAGE!")
except:
    pass
s.close()

print("\n" + "="*60)
print("[*] Test 3: Overflow index field...")
s = socket.socket()
s.settimeout(10)
s.connect(('34.84.25.24', 58554))

s.recv(4096)
s.sendall(b"9999999999999999999\n")
time.sleep(1)

try:
    data = s.recv(8192)
    print(f"Overflow response ({len(data)} bytes):")
    print(data.decode(errors='ignore'))
except:
    pass
s.close()

print("\n" + "="*60)
print("[*] Test 4: Send huge value...")
s = socket.socket()
s.settimeout(10)
s.connect(('34.84.25.24', 58554))

s.recv(4096)
s.sendall(b"0\n")
s.recv(4096)
s.sendall(b"999999999999999999999\n")
s.recv(4096)
s.sendall(b"-1\n")
time.sleep(1)

try:
    data = s.recv(8192)
    print(f"Huge value response ({len(data)} bytes):")
    print(data.decode(errors='ignore'))
except:
    pass
s.close()
