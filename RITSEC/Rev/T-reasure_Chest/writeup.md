# Challenge Writeup: Treasure Chest

* **Category:** Reverse Engineering
* **Flag:** `RS{oh_its_a_TEAreasure_chest}`

## 1. Initial Analysis
Đầu tiên, chúng ta kiểm tra thông tin file bằng lệnh `file` và `strings` trên Kali Linux:
* [cite_start]**File type:** ELF 64-bit LSB executable, biên dịch bằng GCC 14.3.0[cite: 1, 10].
* [cite_start]**Suspicious Strings:** Xuất hiện các chuỗi thông báo như `"Try to open the chest!"`, `"Maybe try saying the magic word:"` và đặc biệt là chuỗi `"tiny_encrypt_key"`[cite: 1, 2].

[cite_start]Việc xuất hiện chuỗi `"tiny_encrypt_key"` gợi ý rất mạnh rằng chương trình sử dụng thuật toán **TEA (Tiny Encryption Algorithm)**[cite: 1].

## 2. Static Analysis
Mở file bằng IDA, chúng ta phân tích hàm `main` và các hàm con:

### Hàm Main (`0x40131B`)
* Chương trình yêu cầu người dùng nhập chuỗi thông qua `fgets`.
* Input được tính toán độ dài và thực hiện căn chỉnh (padding) để đảm bảo là bội số của 8 byte.
* Khóa mã hóa (Key) được gán vào stack: `tiny_encrypt_key`.
* Kết quả sau khi mã hóa được so sánh với một mảng dữ liệu mẫu tại địa chỉ `0x404080` bằng hàm `memcmp` với độ dài **34 byte**.

### Hàm Mã Hóa TEA (`0x4011C6`)
Tại hàm `sub_4011C6`, chúng ta tìm thấy hằng số Delta đặc trưng của TEA:
> `mov [rbp+var_C], 9E3779B9h`

Hàm này thực hiện vòng lặp mã hóa 32 lần trên mỗi khối 8 byte dữ liệu nhập vào.

## 3. Data Extraction
Trích xuất mảng ciphertext (kết quả mong đợi) từ phân đoạn `.data` tại địa chỉ `0x404080`:
`38 75 5B CB 44 D2 BE 5D 96 9C 56 43 EA 98 06 75 4A 48 13 E6 D4 E8 8E 4F 72 70 8B FF DC 99 F8 76 C5 C9`

## 4. Solution Script
Sử dụng Python để viết script giải mã ngược thuật toán TEA với Key và Ciphertext đã tìm được:

```python
import struct

def decrypt(v, k):
    v0, v1 = struct.unpack("<II", v)
    k0, k1, k2, k3 = k
    delta = 0x9E3779B9
    sum_val = (delta * 32) & 0xffffffff
    
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum_val) ^ ((v0 >> 5) + k3))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum_val) ^ ((v1 >> 5) + k1))) & 0xffffffff
        sum_val = (sum_val - delta) & 0xffffffff
        
    return struct.pack("<II", v0, v1)

# Key: tiny_encrypt_key
key = struct.unpack("<IIII", b"tiny_encrypt_key")

# Ciphertext trích xuất từ 0x404080 (đã đệm đủ khối 8 byte)
ciphertext = bytes.fromhex("38755BCB44D2BE5D969C5643EA9806754A4813E6D4E88E4F72708BFFDC99F876C5C9000000000000")

flag = b""
for i in range(0, 40, 8):
    flag += decrypt(ciphertext[i:i+8], key)

print(f"Flag: {flag[:34].decode()}")
```

## 5. Flag 
Chạy solve.py ta sẽ thu được flag
**Flag:** `RS{oh_its_a_TEAreasure_chest}`

