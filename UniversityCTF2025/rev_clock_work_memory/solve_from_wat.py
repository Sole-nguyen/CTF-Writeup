#!/usr/bin/env python3

print("="*60)
print("Phân tích từ file pocketwatch.wat")
print("="*60)

# Từ file WAT, dòng 16-17:
# i32.const 1262702420
# i32.store offset=27 align=1

# Giá trị key được lưu: 1262702420 (decimal)
key_value = 1262702420

print(f"\nGiá trị key (decimal): {key_value}")
print(f"Giá trị key (hex): 0x{key_value:08x}")

# Chuyển sang bytes (little-endian như WASM sử dụng)
key_bytes = key_value.to_bytes(4, 'little')
print(f"Key bytes (little-endian): {key_bytes.hex()} = {key_bytes}")

# Từ dòng 107 - dữ liệu được mã hóa:
# (data (;0;) (i32.const 1024) "\1c\1b\010#{0&\0b=p=\0b~0\147\7fs'un>")

# Chuyển escape sequences thành bytes
encrypted_wat = b"\x1c\x1b\x01" + b"0#{0&\x0b=p=\x0b~0" + b"\x67\x7fs'un>"
print(f"\nDữ liệu mã hóa từ WAT: {encrypted_wat.hex()}")
print(f"Độ dài: {len(encrypted_wat)} bytes")

# Thuật toán giải mã từ WAT:
# Loop từ i=0 đến i=22:
#   decrypted[i] = key[i & 3] XOR encrypted[i]

print("\nGiải mã:")
decrypted = []
for i in range(len(encrypted_wat)):
    key_byte = key_bytes[i & 3]  # i & 3 = i % 4
    plain_byte = encrypted_wat[i] ^ key_byte
    decrypted.append(plain_byte)
    char = chr(plain_byte) if 32 <= plain_byte < 127 else '?'
    print(f"  [{i:2d}] enc=0x{encrypted_wat[i]:02x} XOR key[{i&3}]=0x{key_byte:02x} = 0x{plain_byte:02x} '{char}'")

flag = bytes(decrypted)
print(f"\n{'='*60}")
print(f"FLAG: {flag.decode('ascii')}")
print(f"{'='*60}")
