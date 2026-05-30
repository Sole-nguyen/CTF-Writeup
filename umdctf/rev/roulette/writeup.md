# roulette — UMDCTF (rev)

> **Flag:** `UMDCTF{I_R3ALLY-want-to-pl4y-the-p0werball,+but-my-d4d-said-no-so-im-b3tting-ill-win-on-POLYMARKETinstead}`

---

## Tổng quan

Binary ELF 64-bit mô phỏng trò chơi roulette. Người dùng phải nhập đúng "roulette number" để nhận phản hồi `accepted`. Input hợp lệ chính là **flag**.

---

## Phân tích tĩnh (IDA / Ghidra)

### 1. Đọc input

```c
fgets(buf, 108, stdin);
```

- Buffer tối đa 108 bytes, nhưng verifier yêu cầu **đúng 106 bytes** (sau khi strip `\n`).
- Nếu sai độ dài → reject ngay.

### 2. Cấu trúc verifier — 27 vòng lặp

```
for i in 0..26:
    eax = <giá trị tính từ hằng số nội bộ>  ; hoàn toàn deterministic
    if i < 26:
        cmp  DWORD PTR [buf + 4*i],  eax     ; so sánh 4 bytes
    else:
        cmp  WORD  PTR [buf + 104],  ax      ; vòng cuối: 2 bytes
    jne  fail
```

- **Không có crypto, không có random** — mọi `eax` đều là hằng số được tính từ bảng nội bộ (hardcoded trong binary).
- Vì chỉ là linear comparison, ta chỉ cần **đọc giá trị kỳ vọng** từ mỗi vòng.

### 3. Mapping input → chunks

| Vòng `i` | So sánh với | Bytes trong payload |
|:--------:|:-----------:|:-------------------:|
| 0 – 25   | `u32` LE    | `[4i : 4i+4]`       |
| 26       | `u16` LE    | `[104 : 106]`       |

Tổng: 26 × 4 + 2 = **106 bytes** ✓

---

## Kỹ thuật giải

### Bước 1 — Dump giá trị kỳ vọng

Đặt breakpoint tại từng lệnh `cmp` trong vòng lặp (GDB / IDA debugger), đọc giá trị `eax`/`ax`. Hoặc đọc thẳng bảng hardcoded trong IDA:

```
REQUIRED_CHUNKS = [
    1128549717, 1232815700, 1093882463,  760826956, 1953390967,  762278957, 2033478768,
    1701344301, 1999663149, 1633841765,  724331628,  762606946, 1680701805, 1932354612,
     761555297, 1932357486, 1835609455, 1949524525, 1735289204, 1819044141, 1852405549,
     762212141, 1498173264, 1263681869, 1852396613, 1634038899,      32100,
]
```

### Bước 2 — Ghép thành payload 106 bytes

```python
payload = b""
for i, v in enumerate(REQUIRED_CHUNKS):
    if i < 26:
        payload += v.to_bytes(4, "little")   # 4 bytes LE
    else:
        payload += (v & 0xFFFF).to_bytes(2, "little")  # 2 bytes LE
```

### Bước 3 — Verify

```
REQUIRED_CHUNKS → bytes (LE) → decode ASCII:
  "UMDCTF{I_R3ALLY-want-to-pl4y-the-p0werball,+but-my-d4d-said-no-so-im-b3tting-ill-win-on-POLYMARKETinstead}"
```

Đây chính là flag! Input hợp lệ là flag được encode dưới dạng chuỗi integer little-endian.

---

## Chạy solve

```bash
python3 solve.py
```

### Output

```
[*] Payload length : 106 bytes
[*] Flag           : UMDCTF{I_R3ALLY-want-to-pl4y-the-p0werball,+but-my-d4d-said-no-so-im-b3tting-ill-win-on-POLYMARKETinstead}

[*] Chạy binary...
lets go gambling!
submit roulette number:
accepted
```

---

## Takeaway

- Binary không dùng crypto hay random — verifier là **pure linear comparison**.
- Input kỳ vọng được hardcode dưới dạng hằng số trong binary, chỉ cần dump ra là xong.
- Flag dài 106 bytes, được chia 27 chunk (26×4 + 1×2) và so sánh trực tiếp.
