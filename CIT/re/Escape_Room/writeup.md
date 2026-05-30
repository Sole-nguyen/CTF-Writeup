# Escape Room - Writeup

## 1) Khảo sát nhanh

Binary `escaperoom` là ELF64, menu tương tác:

1. read log
2. toggle lights
3. cycle vents
4. rotate cameras
5. apply door patch
6. toggle battery bridge
7. maintenance shell
8. enter override token

## 2) Điều kiện “room aligned”

Từ hàm `roomAligned()`:

- lights = OFF
- vent route = 1 (east bypass)
- camera bus = 3 (mirror relay)
- door patch count = 2
- battery bridge = ENGAGED
- inspection/mirror flag = true
- alarm muted flag = true

=> Chuỗi thao tác đạt đúng state:

```text
2          # lights OFF
3          # vents -> east bypass
4 4 4      # camera -> bus 3
5 5        # patch count = 2
6          # battery engaged
7 -> mirror -> hush -> back
```

## 3) Sinh override token

`buildOverrideToken()` dùng:

- `roomSignature()` (32-bit signature từ state)
- XOR hằng `0x6f70656e`
- PRNG bước lặp: `seed = seed*0x19660d + spice[i] + 0x3c6ef35f`
- ký tự lấy từ `(seed >> 27) & 0x1f` trên alphabet:
  `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`
- format `XXX-XXX-XXXX`

Với state đã align ở trên, token tính ra:

- **`RHY-QVT-KAXJ`**

## 4) Submit

Nhập token trong menu option `8`:

```text
override token> RHY-QVT-KAXJ
```

Kết quả:

`CIT{Vc282vlhCxIJ}`

## Flag

`CIT{Vc282vlhCxIJ}`

