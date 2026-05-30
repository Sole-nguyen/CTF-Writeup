```markdown
# Writeup: o-nion or a-nion
**CTF:** THEMCTF  
**Category:** Misc  
**Tags:** `Encoding`, `Bases`, `DNA Cipher`, `Custom Scripting`

---

## 📝 Tóm tắt ý tưởng
Tên thử thách "o-nion or a-nion" là một gợi ý chơi chữ tuyệt vời: 
* **o-nion** (củ hành): Ám chỉ việc dữ liệu bị bọc trong rất nhiều lớp mã hóa khác nhau.
* **a-nion** (ion âm / base): Ám chỉ việc các lớp mã hóa này là các hệ cơ số (Base encodings) và base di truyền (DNA bases).

Dữ liệu đầu vào là một chuỗi dài các emoji động vật. Quá trình giải bài gồm 3 giai đoạn chính: giải mã Emoji, bóc tách các lớp Base, và dịch mã DNA Amino Acid.

---

## 🔍 Chi tiết các bước giải

### Bước 1: Giải mã lớp Emoji
Chuỗi cung cấp (ví dụ: `🐭👪🐗🐫🐯...`) gồm toàn các emoji nằm trong block Unicode `U+1F400`. Bằng cách trừ đi giá trị `0x1F400`, ta thu được một ánh xạ rõ ràng:
* Biểu tượng lợn rừng (`🐗`, `0x1F417`) dịch ra `0x17`, đóng vai trò là dấu cách (space).
* Các emoji khác dịch ra các mã ASCII tương ứng với các ký tự hex từ `0-9` và `a-f`. 
* Khi chuyển đổi lại các cặp hex này thành ASCII, ta thu được một chuỗi **Base62**.

**Script Python giải mã lớp 1:**
```python
def extract_emoji_layer(emoji_cipher):
    hex_str = ""
    for char in emoji_cipher:
        val = ord(char) - 0x1f400
        if val == 0x17: # 🐗 là dấu cách
            hex_str += " "
        elif 0x27 <= val <= 0x30: # Số 0-9
            hex_str += str(val - 0x27)
        elif 0x65 <= val <= 0x6a: # Chữ a-f
            hex_str += chr(val - 0x65 + ord('a'))

    # Chuyển Hex sang ASCII
    return "".join([chr(int(h, 16)) for h in hex_str.split()])

with open("emoji.txt", "r", encoding="utf-8") as f:
    cipher = f.read().strip()
    base62_str = extract_emoji_layer(cipher)
    print(base62_str)

```

**Output:** `oHBnFiWdx4lOO221MKPSPfnwHdC9kV3NMnbosDDYQqw...`

---

### Bước 2: Bóc các lớp "Hành" (Base Decoding)

Chuỗi kết quả từ Bước 1 là Base62. Vì đặc thù của bài là các lớp Base bị xáo trộn, ta cần lần lượt thử và bóc tách chúng qua nhiều bước:

1. **Base62** -> decode ra chuỗi có dấu `+` và alphanumeric viết hoa.
2. **Base45** (đặc trưng bởi alphanumeric viết hoa + một vài ký tự đặc biệt) -> decode ra chuỗi toàn viết hoa.
3. **Base32** -> decode ra chuỗi có viết hoa, viết thường và số.
4. **Base64** -> decode ra lớp cuối cùng.

**Script Python bóc tách tự động:**

```python
import base64
import base62 # pip install pybase62
import base45 # pip install base45

# Đưa chuỗi base62 lấy được từ bước 1 vào đây
cipher_base62 = "oHBnFiWdx4lOO221..." 

layer2 = base62.decodebytes(cipher_base62).decode('utf-8')
layer3 = base45.b45decode(layer2).decode('utf-8')
layer4 = base64.b32decode(layer3).decode('utf-8')
final_layer = base64.b64decode(layer4).decode('utf-8')

print(final_layer)

```

**Output:** `TGGGAAATAAGGGAC GCTCACCAC OAATATAOAAT OGATTTTUTCCTGTGCGACAATTOAAC`

---

### Bước 3: Dịch mã DNA Amino Acid

Lớp cuối cùng thoạt nhìn là DNA (A, C, G, T), nhưng lại có lẫn các chữ `O` và `U`. Đây là một thủ thuật giấu tin (Obfuscation):

* Các chữ `O` và `U` là **plaintext** (giữ nguyên không dịch).
* Các chuỗi DNA còn lại được dịch thành **Amino Acid** theo từng bộ ba (Codon).

Dựa vào bảng Amino Acid chuẩn và mã IUPAC mở rộng (với Codon `GAT` mã hóa cho chữ `B` - Asx/Aspartic acid thay vì `D` để tạo thành từ có nghĩa):

| Cụm từ | Phân tách Codon | Dịch mã Amino Acid / Plaintext | Kết quả |
| --- | --- | --- | --- |
| **Từ 1** | `TGG`-`GAA`-`ATA`-`AGG`-`GAC` | Trp(**W**) - Glu(**E**) - Ile(**I**) - Arg(**R**) - Asp(**D**) | `WEIRD` |
| **Từ 2** | `GCT`-`CAC`-`CAC` | Ala(**A**) - His(**H**) - His(**H**) | `AHH` |
| **Từ 3** | `O`-`AAT`-`ATA`-`O`-`AAT` | **O** - Asn(**N**) - Ile(**I**) - **O** - Asn(**N**) | `ONION` |
| **Từ 4** | `O`-`GAT`-`TTT`-`U`-`TCC`-`TGT`-`GCG`-`ACA`-`ATT`-`O`-`AAC` | **O** - Asx(**B**) - Phe(**F**) - **U** - Ser(**S**) - Cys(**C**) - Ala(**A**) - Thr(**T**) - Ile(**I**) - **O** - Asn(**N**) | `OBFUSCATION` |

Ghép các từ lại và ngăn cách bằng dấu gạch dưới `_`, ta được nội dung của flag.

---

## 🚩 Flag

`THEM?!CTF{weird_ahh_onion_obfuscation}`

```

```