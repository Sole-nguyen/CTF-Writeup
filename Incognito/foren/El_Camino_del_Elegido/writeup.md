# Writeup – Lattice / Hidden Path (Flag: `iiitl{...}`)

## 1) Đề bài & file được cung cấp
Trong thư mục challenge có:
- `rules.txt`: thơ/ẩn dụ gợi ý quy tắc.
- `echo.png`: chứa một ma trận số (3×3).
- `nodes.json`: dữ liệu đồ thị rất lớn (~437MB) gồm ~1,000,000 node.
- Tên thư mục: `YSBtb2QgYiA9IDA` (trông như Base64).

Flag format: `iiitl{...}`.

---

## 2) Phân tích hint trong `rules.txt`
Nội dung chính (tóm ý):
- “lattice of six-fold grace, a million souls”: ám chỉ một lưới (grid/lattice) có ~1 triệu điểm.
- “Most wander lost… false connections”: đồ thị có rất nhiều cạnh “nhiễu”.
- “The path of triumph… rhythm… constant creed”: có một đường đi đúng mang tính **deterministic** (theo một nhịp/khẩu quyết cố định).
- “A numerical echo, a hidden key”: có một **con số khóa** ẩn trong `echo.png`.
- “Ignore the noise”: bỏ qua các cạnh nhiễu, chỉ theo đúng quy tắc.

---

## 3) Hint ẩn từ tên thư mục (Base64)
Tên thư mục `YSBtb2QgYiA9IDA` decode Base64 ra:

```
a mod b = 0
```

Nghĩa: một điều kiện kiểu **chia hết** (modulo) sẽ là chìa khóa để chọn đường đi đúng.

---

## 4) Phân tích `echo.png` → tìm “hidden key”
`echo.png` chứa ma trận:

\[
\begin{bmatrix}
7 & 233 & 95\\
0 & 191 & -4\\
7 & 233 & 96
\end{bmatrix}
\]

Bước quan trọng là lấy **determinant** của ma trận này.

Khi tính determinant ta được:

- **det(M) = 1337**

`1337` chính là “numerical echo / hidden key”. Đây cũng liên hệ rất đẹp với văn hóa CTF (leet).

---

## 5) Hiểu cấu trúc `nodes.json`
### 5.1 Dạng dữ liệu
`nodes.json` là một mảng JSON cực lớn, mỗi dòng (sau dòng `[` đầu) là **một object node** (JSON object) và thường kết thúc bằng dấu phẩy `,`.

Mỗi node có dạng:
```json
{
  "id": 1,
  "coords": [x, y],
  "neighbors": [
    {"to": 586266, "weight": 329.4537},
    ...
  ]
}
```

- `id`: chỉ số node.
- `coords`: toạ độ trên lưới.
- `neighbors`: danh sách cạnh đi ra.
  - `to`: id đích.
  - `weight`: trọng số (số thực).

### 5.2 “A million souls”
Kiểm tra nhanh số dòng cho thấy file có khoảng 1,000,002 dòng (1 dòng `[` + 1,000,000 node + 1 dòng `]`).

Quan sát mapping `id -> coords` thấy:
- `id=1` có `coords=[0,0]`.
- `id=1000` có `coords=[999,0]`.
- `id=1001` có `coords=[0,1]`.

Suy ra quy luật toạ độ theo hàng:
- `id = y*1000 + x + 1` với `0 ≤ x,y < 1000`.

=> Đúng với hint “lattice” (lưới 1000×1000 = 1,000,000 điểm).

---

## 6) Tìm “slender thread” – đường đi mảnh
Đồ thị có rất nhiều cạnh ngẫu nhiên (noise). Cần một tiêu chí để “ignore the noise”.

### 6.1 Dùng gợi ý “a mod b = 0” + key 1337
Ta thử áp điều kiện **chia hết** với `1337` lên `id`.

Ý tưởng:
- Xét các node có `id % 1337 == 0` (id là bội của 1337).
- Trong danh sách `neighbors` của một node đặc biệt như vậy, ta tìm cạnh đi tới node cũng có `to % 1337 == 0`.

Quan sát thực nghiệm (rất quan trọng):
- Với các node `id` là bội của 1337, thường có đúng **1** neighbor cũng là bội của 1337.
- Điều này tạo thành một chuỗi (chain) rất “mảnh”: mỗi bước chỉ có 1 lựa chọn đúng.

Đây chính là “slender thread”.

### 6.2 Trọng số `weight` là ASCII
Khi lần theo chuỗi bội của 1337, ta thấy `weight` trông giống số nguyên (hoặc gần nguyên).

Nếu lấy `chr(round(weight))`, ta nhận được ký tự ASCII và các ký tự ghép lại tạo thành chuỗi bắt đầu bằng `iiitl{...}`.

---

## 7) Giải bằng script (Python, streaming, không load 437MB vào RAM)
Vì `nodes.json` rất lớn, không thể `json.load()` cả file.

Ta parse **từng dòng**, chỉ lưu các node cần thiết (id bội của 1337) và cạnh đặc biệt của nó.

### Script solve
```python
import json

PATH = "nodes.json"
MOD = 1337

special = {}  # id -> (next_id, weight)

with open(PATH, "r", encoding="utf-8") as f:
    assert f.readline().strip() == "["
    for line in f:
        line = line.strip()
        if line == "]":
            break
        if line.endswith(","):
            line = line[:-1]

        obj = json.loads(line)
        i = obj["id"]
        if i % MOD != 0:
            continue

        # tìm neighbor có to cũng là bội của 1337
        hits = [nb for nb in obj["neighbors"] if nb["to"] % MOD == 0]
        if len(hits) == 1:
            nb = hits[0]
            special[i] = (nb["to"], nb["weight"])

# traverse bắt đầu từ 1337
cur = MOD
out = []
seen = set()

while cur in special and cur not in seen:
    seen.add(cur)
    nxt, w = special[cur]
    out.append(chr(int(round(w))))
    cur = nxt
    if out and out[-1] == '}':
        break

print("".join(out))
```

### Output
Chạy script sẽ in ra:

```
iiitl{1h3re_i5_4lways_4_p41h_w4i1ing_t0_b3_d1scov3red}
```

---

## 8) Flag
**Flag:**

`iiitl{1h3re_i5_4lways_4_p41h_w4i1ing_t0_b3_d1scov3red}`

---

## 9) Vì sao cách này “đúng” theo hint?
- “A million souls”: lưới 1000×1000.
- “false connections”: neighbor list dày, ngẫu nhiên.
- “hidden key”: determinant của ma trận = 1337.
- “a mod b = 0”: lọc node/cạnh theo điều kiện chia hết.
- “slender thread”: mỗi node bội 1337 có đúng 1 cạnh tiếp tục sang bội 1337 → đường đi duy nhất.
- “numerical echo”: `weight` chính là “echo” (mã ASCII) phát ra trên đường đi.

---

## 10) Notes / pitfalls
- Không nên grep toàn bộ file để tìm flag trực tiếp: `nodes.json` không chứa string `iiitl{`.
- Tránh load toàn bộ JSON vào RAM (437MB + overhead sẽ rất nặng). Streaming line-by-line là tối ưu.
- Dữ liệu là JSON array nhưng mỗi element nằm trên **một dòng rất dài**, vì thế đọc theo dòng là hợp lý.
