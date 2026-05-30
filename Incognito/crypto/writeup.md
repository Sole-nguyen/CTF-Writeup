# PDF stego — “Look it’s a plane… a jet… a bird”

**File:** `Untitled_document.pdf`  
**SHA256:** `4e96a1a043ae5426448852ecbaa25af26fdc7dc1b83e2f70749f574a13dbe219`  
**Flag:** `IIITL{this_was_annoying_lol_79823979735}`

---

## 1) Recon nhanh: flag không nằm trong text thường
PDF này (Google Docs renderer) gần như chỉ vẽ bằng ảnh nhỏ (XObject images). Dùng `pypdf`/`strings` sẽ không thấy `IIITL{...}` trực tiếp.

Điểm bất thường nằm ở **metadata**:

```bash
exiftool -Keywords -Subject -Title -Producer Untitled_document.pdf
```

Output (rút gọn):

- `Keywords: What is this?`
- `Subject: 0010010100100110...` (chuỗi chỉ gồm `0/1`, dài **320 bit**)

=> `/Subject` là ciphertext được viết dưới dạng **bitstring**.

---

## 2) Lấy “key” từ hình các con chim (XObject images)
### 2.1. Trích xuất các ảnh nhúng trong PDF
Trang PDF dùng nhiều `/XObject` kiểu `/Image` và có `/SMask` (alpha mask). Ta render từng XObject thành PNG.

Python (pypdf + Pillow):

```py
from PIL import Image
from pypdf import PdfReader
from pypdf.filters import decode_stream_data
import os

r = PdfReader('Untitled_document.pdf')
page = r.pages[0]
xobj = page['/Resources']['/XObject'].get_object()

os.makedirs('rendered', exist_ok=True)
for name, ref in xobj.items():
    obj = ref.get_object()
    if obj.get('/Subtype') != '/Image':
        continue

    w, h = int(obj['/Width']), int(obj['/Height'])
    rgb = decode_stream_data(obj)
    img = Image.frombytes('RGB', (w, h), rgb)

    sm = obj.get('/SMask')
    if sm:
        sm = sm.get_object()
        a = decode_stream_data(sm)
        alpha = Image.frombytes('L', (int(sm['/Width']), int(sm['/Height'])), a)
        if alpha.size != img.size:
            alpha = alpha.resize(img.size)
        img = img.convert('RGBA')
        img.putalpha(alpha)
    else:
        img = img.convert('RGBA')

    img.save(f'rendered/{name[1:]}.png')
```

### 2.2. Ghép đúng thứ tự vẽ
Thứ tự vẽ nằm trong content stream của trang, theo toán tử `Do`:

```py
import re
content = page.get_contents().get_data().decode('latin1', 'replace')
order = re.findall(r'/(X\d+)\s+Do', content)
```

Ghép các ảnh theo `order` sẽ tạo ra `combined.png`.

### 2.3. Bit-plane: chữ ẩn trong ảnh
Các glyph/“chim” có dữ liệu ẩn theo **bit-plane** (đặc biệt ở LSB). Khi tách bit-plane kênh màu và quan sát, ta đọc được:

> `LOOKSLIKEAKEYTOME`

Câu này nghĩa là “trông giống một cái key”, và key thực tế dùng để XOR là:

> `lookslikeakeytome` (đưa về lowercase để dùng trực tiếp)

---

## 3) `/Subject` bitstring → 40 bytes ciphertext
`/Subject` dài 320 bit => 40 bytes.

```py
import subprocess
subj = subprocess.check_output(
    ['exiftool','-s','-s','-s','-Subject','Untitled_document.pdf'],
    text=True
).strip()

ct = bytes(int(subj[i:i+8], 2) for i in range(0, len(subj), 8))
print(len(ct))  # 40
```

Ciphertext (hex):

```
2526263f3f171d030c1234121807300c0b020016021d0b36070a0d3452404c5d5e5c5b5658584611
```

---

## 4) Giải mã: XOR lặp key
XOR lặp theo key `lookslikeakeytome`:

```py
key = b'lookslikeakeytome'
pt = bytes(c ^ key[i % len(key)] for i, c in enumerate(ct))
print(pt.decode('ascii'))
```

Output ra thẳng flag:

```
IIITL{this_was_annoying_lol_79823979735}
```

### Note (vì sao có case/ngoặc “lạ” nếu dùng key uppercase?)
Nếu dùng `LOOKSLIKEAKEYTOME` (uppercase) thì plaintext sẽ bị lệch “bit 0x20” (ASCII case-bit), làm ra dạng `iiitl[THIS...`.
Khi đó XOR thêm `0x20` toàn bộ byte sẽ quay về đúng:

- `i ^ 0x20 = I`
- `[` (0x5b) ^ 0x20 = `{` (0x7b)
- `]` (0x5d) ^ 0x20 = `}` (0x7d)

Cách đơn giản nhất: dùng luôn key lowercase `lookslikeakeytome` để ra flag trực tiếp.

---

## 5) Kết luận
- Flag không nằm trong text hiển thị.
- “Chim”/glyph images giấu **key** bằng bit-plane.
- `/Subject` chứa ciphertext dạng bitstring.
- XOR với key => flag.

**Flag:** `IIITL{this_was_annoying_lol_79823979735}`
