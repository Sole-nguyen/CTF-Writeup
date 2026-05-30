#!/usr/bin/env python3

# Phân tích cẩn thận escape sequence từ WAT
# (data (;0;) (i32.const 1024) "\1c\1b\010#{0&\0b=p=\0b~0\147\7fs'un>")

# \1c = 0x1c
# \1b = 0x1b
# \01 = 0x01
# 0 = '0' = 0x30
# # = '#' = 0x23
# { = '{' = 0x7b
# 0 = '0' = 0x30
# & = '&' = 0x26
# \0b = 0x0b
# = = '=' = 0x3d
# p = 'p' = 0x70
# = = '=' = 0x3d
# \0b = 0x0b
# ~ = '~' = 0x7e
# 0 = '0' = 0x30
# \14 = 0x14 !!!  KHÔNG PHẢI \147
# 7 = '7' = 0x37
# \7f = 0x7f
# s = 's' = 0x73
# ' = '\'' = 0x27
# u = 'u' = 0x75
# n = 'n' = 0x6e
# > = '>' = 0x3e

# Đợi, để tôi đọc lại: "\147" - đây là octal!
# \147 trong octal = 103 decimal = 0x67

# Vậy chuỗi đầy đủ là:
encrypted_hex = "1c1b0130237b30260b3d703d0b7e30" + "14" + "377f7327756e3e"
print(f"Nếu \\147 là một ký tự (octal 147 = hex 67): {encrypted_hex}")

encrypted = bytes.fromhex(encrypted_hex)
print(f"Độ dài: {len(encrypted)} bytes")

# Nhưng cũng có thể là:
# \14 (octal 14 = hex 0C) + 7
encrypted_hex2 = "1c1b0130237b30260b3d703d0b7e30" + "0c" + "377f7327756e3e"
print(f"\nNếu \\14 (octal) + '7': {encrypted_hex2}")
encrypted2 = bytes.fromhex(encrypted_hex2)
print(f"Độ dài: {len(encrypted2)} bytes")

# Thử cả hai:
key_value = 1262702420
key_bytes = key_value.to_bytes(4, 'little')
print(f"\nKey: {key_bytes} = {key_bytes.hex()}")

print("\n" + "="*60)
print("Thử 1: \\147 là một ký tự octal")
print("="*60)
flag1 = bytes([encrypted[i] ^ key_bytes[i & 3] for i in range(len(encrypted))])
print(f"Decrypted: {flag1}")
print(f"As text: {flag1.decode('ascii', errors='replace')}")

print("\n" + "="*60)
print("Thử 2: \\14 + '7' riêng biệt")  
print("="*60)
flag2 = bytes([encrypted2[i] ^ key_bytes[i & 3] for i in range(len(encrypted2))])
print(f"Decrypted: {flag2}")
print(f"As text: {flag2.decode('ascii', errors='replace')}")

# Hãy thử đọc trực tiếp từ file WAT
print("\n" + "="*60)
print("Đọc trực tiếp từ file WAT")
print("="*60)

# Tôi sẽ parse chính xác escape sequence
wat_string = r"\1c\1b\010#{0&\0b=p=\0b~0\147\7fs'un>"
print(f"WAT string: {wat_string}")

# Parse escape sequences
result = []
i = 0
while i < len(wat_string):
    if wat_string[i] == '\\':
        # Escape sequence
        if i+1 < len(wat_string) and wat_string[i+1] in '0123456789':
            # Octal escape
            octal_str = ''
            j = i + 1
            while j < len(wat_string) and j < i + 4 and wat_string[j] in '0123456789':
                octal_str += wat_string[j]
                j += 1
            value = int(octal_str, 8)
            result.append(value)
            i = j
        else:
            # Hex escape?
            i += 1
    else:
        result.append(ord(wat_string[i]))
        i += 1

encrypted3 = bytes(result)
print(f"Parsed: {encrypted3.hex()}")
print(f"Length: {len(encrypted3)}")

flag3 = bytes([encrypted3[i] ^ key_bytes[i & 3] for i in range(len(encrypted3))])
print(f"Decrypted: {flag3}")
try:
    print(f"*** FLAG: {flag3.decode('ascii')} ***")
except:
    print(f"As text: {flag3.decode('ascii', errors='replace')}")
