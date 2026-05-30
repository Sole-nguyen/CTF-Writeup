# Brick by Brick (UART) — Writeup

## Tệp
- `code.csv` (timestamp, logic_level)

## Phân tích
1. Khoảng lấy mẫu cố định: khoảng 29.96 µs → sampling rate ~33.3 kHz.
2. Start bit là cạnh xuống (1 → 0), đúng kiểu UART 8N1.
3. Chọn baud sao cho mỗi bit xấp xỉ 1 sample/bit → baud ~33,333.

## Giải mã
Giải mã UART 8N1, LSB-first, lấy mẫu ở giữa bit. Kết quả là log boot Linux và dòng:

```
secretflag: 554d4153537b553452375f31355f3768335f623335372c5f72316768373f7d
```

Giải mã hex → ASCII:

```
UMASS{U4R7_15_7h3_b357,_r1gh7?}
```

## Flag
`UMASS{U4R7_15_7h3_b357,_r1gh7?}`
