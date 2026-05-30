#!/usr/bin/env python3
"""
Hexadecimal byte-level analysis
"""

with open('flag.raw', 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes\n")

# Show first 200 bytes in hex
print("First 200 bytes (hex):")
for i in range(0, min(200, len(data)), 16):
    hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
    print(f"{i:04x}: {hex_part:<48} {ascii_part}")

# Byte frequency
from collections import Counter
freq = Counter(data)
print(f"\n\nByte frequency (top 30):")
print("Rank | Hex  | Dec | ASCII | Count | Percentage")
print("-" * 60)
for i, (byte, count) in enumerate(freq.most_common(30)):
    ascii_char = chr(byte) if 32 <= byte < 127 else '.'
    percent = count * 100.0 / len(data)
    print(f"{i:4d} | 0x{byte:02x} | {byte:3d} | '{ascii_char}'   | {count:6d} | {percent:5.2f}%")

# Check for patterns
print("\n\nLooking for repeating byte sequences...")
for length in [2, 3, 4]:
    patterns = Counter([data[i:i+length] for i in range(len(data)-length)])
    print(f"\nTop {length}-byte patterns:")
    for pattern, count in patterns.most_common(5):
        hex_str = ' '.join(f'{b:02x}' for b in pattern)
        print(f"  {hex_str}: {count} times")

# Check if it's a simple XOR
print("\n\nChecking for XOR patterns...")
print("If ASIS{ is at the start, XOR key would be:")
target = b'ASIS{'
for i in range(min(5, len(data))):
    if i < len(target):
        xor_key = data[i] ^ target[i]
        print(f"  Position {i}: 0x{data[i]:02x} ^ 0x{target[i]:02x} = 0x{xor_key:02x} ('{chr(xor_key) if 32 <= xor_key < 127 else '?'}')")
