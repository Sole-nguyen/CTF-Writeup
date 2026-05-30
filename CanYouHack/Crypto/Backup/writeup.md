# Backup - Crypto Writeup

Ý tưởng chính là lộ nonce dạng `r1 = r + a`, `r2 = r + b` với `a, b` chỉ cỡ ~125 bit.

Từ chữ ký:

- `s1 = r1 + x1*h (mod q)`
- `s2 = r2 + x2*h (mod q)`

Suy ra:

`(s1 - s2) = (a - b) + (x1 - x2)*h (mod q)`

Đặt `d = x1 - x2`, `e = a - b` thì mỗi message cho một phương trình:

`t_i = d*h_i + e_i (mod q)`, với `|e_i|` nhỏ.

Lấy 2 chữ ký, khử `d`:

`h2*e1 - h1*e2 = h1*t2 - h2*t1 (mod q)`.

Đây là Hidden Number Problem nhỏ chiều, giải bằng lattice (2D CVP/LLL) để tìm `e1`, rồi suy ra `d`.

Sau đó key AES chính là:

`key = hash([d]).to_bytes(32, "big")`

Decrypt ciphertext trong message thứ hai sẽ ra flag:

`BtSCTF{b3_c4r3fu1_wi7h_sm4ll_numb3rs!_C0pp3rsm1th_FTW}`

File `solve.py` đã tự động làm toàn bộ bước trên và in flag.
