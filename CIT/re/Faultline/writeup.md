# Faultline - Writeup

## 1) Khảo sát nhanh

Binary `faultline` là ELF64, không strip, có các lệnh:

- `score <PROFILE>`
- `trace <PROFILE>`
- `token <PROFILE>`
- `submit <PROFILE> <TOKEN>`

Alphabet profile: `BCDFGHJKLMNPQRST` (16 ký tự), độ dài profile = 12.

## 2) Ý tưởng chính

Từ disassembly:

- `parseProfile`: map từng ký tự profile -> số `0..15` theo alphabet.
- `computeFaultlineScoreVisible`: tính score từ:
  - `stressTrace` (11 phần tử)
  - `shearTrace` (10 phần tử)
  - `grainTrace` (9 phần tử)
  - `loadMetric` (tổng 12 phần tử)
  - `sealMetric` (tổ hợp tuyến tính mod 16)

Mỗi trace được so với mảng mục tiêu trong `.rodata`:

- `OBS_STRESS = [2,5,11,10,5,1,13,4,3,3,14]`
- `OBS_SHEAR  = [5,5,15,8,5,6,7,4,5,5]`
- `OBS_GRAIN  = [3,11,3,4,14,4,5,6,1]`
- thêm điều kiện `load == 93`, `seal == 9`.

Score tối đa chính là mốc lịch sử `2026`.

## 3) Dựng hệ ràng buộc

Gọi profile số là `p[0..11]`:

- `stress[i] = (2*p[i] + 3*p[i+1]) & 0xf`
- `shear[i]  = p[i] ^ p[i+2]`
- `grain[i]  = (p[i] + p[i+3] - p[i+1]) & 0xf`

Giải brute-force 2 biến đầu (`p0,p1`) rồi suy ra toàn bộ qua chuỗi `shear`, sau đó check toàn bộ điều kiện.

Nghiệm duy nhất:

- `p = [14,2,11,7,4,15,1,9,6,13,3,8]`
- profile: **`SDPKGTCMJRFL`**

## 4) Token và submit

```bash
./faultline score SDPKGTCMJRFL
# 2026 (catastrophic resonance lock)

./faultline token SDPKGTCMJRFL
# Z2L-2F5-BUBP

./faultline submit SDPKGTCMJRFL Z2L-2F5-BUBP
# CIT{12z4PXVTa3x3}
```

## Flag

`CIT{12z4PXVTa3x3}`

