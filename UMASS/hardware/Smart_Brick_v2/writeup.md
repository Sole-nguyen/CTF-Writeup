# Smart Brick v2 (KiCad PCB) — Writeup

## Tệp
- `smart-brick-v2.kicad_pcb`

## Nhận diện
Đây là file PCB của KiCad. Quan sát thấy:
- J1: 7 input `/IN0..IN6` + GND → gợi ý 7-bit ASCII.
- 19 LED (D1–D19) được điều khiển qua MOSFET (Q1–Q19) và điện trở.
- Logic dùng các IC 74LS: 74LS04, 74LS00, 74LS02, 74LS08, 74LS21, 74LS20, 74LS27, 74LS32, 74LS86.

## Ý tưởng giải
1. Parse `.kicad_pcb` để lấy mapping **pad ↔ net**.
2. Mô hình hóa từng IC theo chân chuẩn TTL (boolean gate).
3. Lấy các net điều khiển LED: `/G59 /G62 /G13 /G19 /G21 /G24 /G26 /G29 /G31 /G36 /G39 /G41 /G43 /G45 /G47 /G49 /G52 /G54 /G56`.
4. Brute-force mọi giá trị input 7-bit (0..127), tìm giá trị làm mỗi LED sáng.
5. Vì 74LS27 (triple 3-input NOR) có nhiều cách nhóm chân, brute-force grouping để mỗi LED sáng **duy nhất một input**.

## Kết quả
Grouping đúng cho 74LS27 (out6 dùng pins 3,4,5 và out12 dùng pins 1,2,13) cho chuỗi:

```
UMASS{In_Th3_G4t3s}
```

## Flag
`UMASS{In_Th3_G4t3s}`
