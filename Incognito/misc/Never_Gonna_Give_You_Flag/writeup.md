# Never Gonna Give You Flag — Writeup

## Tóm tắt
Bài này là một chuỗi “trail” gồm:
1) `chall.txt` là file polyglot: phần đầu là code C/C++ “hehe” (đánh lừa), phần sau nhúng một ZIP.
2) ZIP chứa ảnh JPEG có giấu dữ liệu bằng **steghide**, kèm các mảnh header/constant để tìm **passphrase**.
3) Code “hehe” tạo ra một **TinyURL** (bị obfuscate bằng phép toán), URL này cần nhập vào website để nhận 3 mảnh `parts`.
4) Dữ liệu giấu trong ảnh là một **JAR** Java 17, dùng để “Decrypt” 3 mảnh kia ra flag.

Flag: `IIITL{r1ck_45t13y_15_l3g3nd}`

---

## Bước 1 — Nhận diện `chall.txt` không phải text bình thường
Kiểm tra type/magic bytes:

```bash
file chall.txt
python3 - <<'PY'
from pathlib import Path
p=Path('chall.txt')
data=p.read_bytes()
print('PK offset =', data.find(b'PK\x03\x04'))
PY
```

Kết quả cho thấy có signature ZIP `PK\x03\x04` nằm **giữa file** (offset `22157`). Điều này nghĩa là `chall.txt` chứa một ZIP nhúng bên trong.

---

## Bước 2 — Carve ZIP ra khỏi `chall.txt` và giải nén
Cắt từ offset ZIP tới hết file:

```bash
dd if=chall.txt of=payload.zip bs=1 skip=22157 status=none
unzip -l payload.zip
unzip -o payload.zip -d extracted
```

Trong `extracted/x/` có:
- `a`, `b`, `c`: các mảnh code/header
- `hehe.h`: một header “giả”
- `i`: JPEG 500×500

---

## Bước 3 — Lấy passphrase steghide từ các mảnh header
Đọc các mảnh:

```bash
sed -n '1,200p' extracted/x/b
sed -n '1,200p' extracted/x/hehe.h
```

Ta thấy có 2 key khác nhau:
- `extracted/x/b` chứa: `#define IMG_KEY "rickroll_key_123"`
- `extracted/x/hehe.h` chứa: `#define IMG_KEY "random_key_456"`

Thử thực tế với steghide sẽ xác nhận key đúng là `rickroll_key_123`.

---

## Bước 4 — Extract payload giấu trong JPEG bằng steghide
Thử giải stego:

```bash
steghide extract -sf extracted/x/i -p 'rickroll_key_123' -xf secret1.bin
file secret1.bin
unzip -l secret1.bin
```

`secret1.bin` là **JAR** và chứa `Decrypt.class`.

---

## Bước 5 — Giải obfuscation trong code “hehe” để lấy TinyURL
Trong phần code ở `chall.txt` có hàm build string kiểu:

```c
hehe_append("", (char)(haha * haha + 4)) + ...
```

Trong header đúng, `haha = 10`. Tính ra chuỗi:

```bash
python3 - <<'PY'
haha=10
vals=[
  haha*haha + 4,
  haha*haha + 16,
  haha*haha + 16,
  haha*haha + 12,
  haha*haha + 15,
  haha*haha - 42,
  haha*haha - 53,
  haha*haha - 53,
  haha*haha + 16,
  haha*haha + 5,
  haha*haha + 10,
  haha*haha + 21,
  haha*haha + 17,
  haha*haha + 14,
  haha*haha + 8,
  haha*haha - 54,
  haha*haha - 1,
  haha*haha + 11,
  haha*haha + 9,
  haha*haha - 53,
  haha*haha + 3,
  haha*haha - 52,
  haha*haha + 16,
  haha*haha - 55,
  haha*haha + 21,
  haha*haha - 52,
  haha*haha + 17,
  haha*haha - 48,
  haha*haha - 55,
  haha*haha + 17,
  haha*haha + 14,
  haha*haha - 51,
]
print(''.join(map(chr, vals)))
PY
```

Kết quả:

```
https://tinyurl.com/g0t-y0u4-ur1
```

---

## Bước 6 — Phân tích website để biết endpoint và input đúng
Fetch HTML trang `https://rick-roll-0k02.onrender.com/` thấy JS gọi endpoint:

- POST `https://rick-roll-0k02.onrender.com/x7a9kq`
- Body: `{ "input": "..." }`

Gửi TinyURL vào (quan trọng: **phải là TinyURL**, không phải link YouTube sau khi redirect) sẽ nhận `status: correct` và 3 mảnh `parts`:

```bash
curl -s -X POST https://rick-roll-0k02.onrender.com/x7a9kq \
  -H 'Content-Type: application/json' \
  -d '{"input":"https://tinyurl.com/g0t-y0u4-ur1"}'
```

Ví dụ response:

```json
{
  "parts": [
    "ZZZKC{i1tb_45",
    "1721260800224b1d2d245c073e57000807134e58",
    "A01G4P5HSO0}q"
  ],
  "status": "correct"
}
```

---

## Bước 7 — Chạy JAR (Java 17) để decrypt `parts`
JAR được build với Java 17 (class file version 61). Nếu máy chỉ có Java 11 sẽ lỗi `UnsupportedClassVersionError`.

Cách mình làm là tải **portable JRE 17 (Temurin)** về local và chạy:

```bash
# tải JRE 17 portable
curl -L -o jre17.tar.gz \
  'https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jre/hotspot/normal/eclipse'
mkdir -p jre17
tar -xzf jre17.tar.gz -C jre17 --strip-components=1

# chạy tool decrypt (đúng format: "[p1]|[p2]|[p3]")
./jre17/bin/java -jar secret1.bin \
  "[ZZZKC{i1tb_45]|[1721260800224b1d2d245c073e57000807134e58]|[A01G4P5HSO0}q]"
```

Output:

```
IIITL{r1ck_45t13y_15_l3g3nd}0BFU5C4T10N
```

Phần `0BFU5C4T10N` chỉ là “decoy/trailer”, còn flag theo format yêu cầu là:

**`IIITL{r1ck_45t13y_15_l3g3nd}`**
