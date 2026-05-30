# Thunder-Blaze (misc) — THE GAUNTLET

**Remote:** `nc 34.131.216.230 1337`

Service trả về nhiều “Task” liên tiếp và **tổng thời gian chỉ ~1 giây** (“You have 1 second to complete all tasks.”). Vì vậy lời giải phải:

- đọc/parse output theo dòng,
- trả lời ngay khi thấy prompt `> `,
- tránh vòng lặp Python dài (50 triệu bước sẽ chết vì `Alarm clock`).

Flag mình lấy được:

```
IIITL{C_15_41w4y5_f4573r_7h4n_py7h0n_5ad6363ca76d}
```

---

## 1) Task 1 — Warmup (nhân số)

Task 1 dạng:

```
[Task 1] Warmup
Calculate: 3834 * 3899
>
```

Chỉ cần parse hai số và gửi tích.

### Ý tưởng code
- Regex bắt `Calculate: ...`
- `eval` **không an toàn** nếu để server nhét ký tự lạ; nên chỉ cho phép `[0-9+\-*/%() ]` hoặc tự parse.

---

## 2) Task 2 — The Filter (OCR + tính S_50,000,000)

Task 2 cho công thức:

- `S_0 = ...`, `S_1 = ...`
- `S_i = ((S_{i-1} * C) ^ (S_{i-2} + D)) % E`
- `C`, `D`, `E` **không in ra trực tiếp** mà dưới dạng **ASCII-art** 5 dòng.
- Yêu cầu: `Find the value of S_50000000`

Ví dụ (mỗi lần chạy server sẽ random khác):

```
--- VALUE OF C ---
@#*  ##%  @@#  *#*  
#.-  @ %  #    #.#  
##@  %.#  *@*  %:#  
. @  @ #  :.@  *.%  
@*@  #@*  @@%  #**  

--- VALUE OF D ---
...

--- VALUE OF E ---
...
```

### 2.1) Nhận xét về font số
Quan sát thấy:

- Mỗi chữ số là **khối 3×5**.
- Giữa các chữ số có khoảng cách cố định (thực tế mỗi digit chiếm **5 cột**: 3 cột pixel + 2 cột space).
- Các ký tự như `# % @ *` thường là “pixel bật”, còn `space . : -` thường là “pixel tắt”.

=> Có thể OCR bằng cách chuyển mỗi digit thành ma trận bit 3×5 rồi đối chiếu với template 0–9.

### 2.2) OCR: tách glyph và match template

**Bước 1 — đọc đúng 5 dòng** sau mỗi header `--- VALUE OF X ---`.

Lưu ý output từ `nc` có thể chứa `\r\n`, nên cần strip `\r`.

**Bước 2 — tách chữ số theo cột:**

- Với 4 digit (C, D): mỗi dòng dài ~`4 * 5 = 20` (thường có thêm 1 space/CR).
- Với 6 digit (E): mỗi dòng dài ~`6 * 5 = 30`.

Ta lấy digit thứ `i` ở dòng `y` bằng `row[i*5 : i*5+3]`.

**Bước 3 — map ký tự → bit:**

- ON: `# % @ *`
- OFF: `space . : -`

**Bước 4 — so khớp với template 0–9:**

Template tiêu chuẩn (dùng `#` là bật, `.` là tắt), ví dụ:

- `0`
  ```
  ###
  #.#
  #.#
  #.#
  ###
  ```
- `1`
  ```
  ..#
  ..#
  ..#
  ..#
  ..#
  ```
- `2`
  ```
  ###
  ..#
  ###
  #..
  ###
  ```

Match bằng **Hamming distance** (đếm số pixel khác nhau) và lấy digit có distance nhỏ nhất.

### 2.3) Vì sao không thể brute-force 50,000,000 bước trong Python

Nếu tính trực tiếp:

```python
for i in range(2, 50_000_000+1):
    S = ((S_prev*C) ^ (S_prev2+D)) % E
```

thì ~50M iteration sẽ vượt 1 giây (và server kill với `Alarm clock`).

### 2.4) Tối ưu bằng chu kỳ (cycle) của trạng thái

Định nghĩa trạng thái:

```
state_i = (S_{i-1}, S_i)
```

Hàm chuyển trạng thái là xác định:

```
(S_{i-1}, S_i) -> (S_i, ((S_i*C) ^ (S_{i-1}+D)) % E)
```

Vì mọi giá trị đều mod `E`, nên mỗi thành phần thuộc `[0, E-1]`.

=> số trạng thái tối đa là `E^2`. Theo **pigeonhole principle**, dãy trạng thái sẽ lặp lại ⇒ có chu kỳ:

- `mu`: độ dài phần “đuôi” trước khi vào chu kỳ
- `lambda`: độ dài chu kỳ

Khi biết `(mu, lambda)`, ta có thể nhảy tới `S_n` bằng:

- nếu `n < mu`: lấy trực tiếp
- nếu `n >= mu`: dùng chỉ số rút gọn
  ```
  idx = mu + (n - mu) % lambda
  S_n = vals[idx]
  ```

### 2.5) Tại sao vẫn cần C (không chỉ cycle trong Python)

Dù chỉ cần tìm cycle khoảng vài trăm nghìn đến ~1 triệu bước, Python + dict/list vẫn có thể sát nút 1 giây (tuỳ instance). Trong lần chạy thực tế mình thấy Python tính ra đáp án đúng nhưng tốn ~1.1s ⇒ bị timeout.

Vì vậy mình:

- dùng Python để: kết nối `nc`, parse task, OCR C/D/E
- dùng C `-O3` để: tìm cycle + trả `S_50,000,000` cực nhanh

Kết quả: tính `S_50,000,000` ~0.2s ⇒ pass.

---

## 3) Implementation

Repo mình tạo 2 file:

- `s_calc.c`: chương trình C tính `S_n` bằng cycle detection
- `s_calc`: binary compile từ `s_calc.c`

### 3.1) C helper (`s_calc.c`)

Chạy:

```bash
gcc -O3 -march=native -std=c11 -o s_calc s_calc.c
./s_calc S0 S1 C D E n
```

Ý chính:

- Pack state vào `uint64_t` để hash nhanh:
  - vì `E < 1,000,000` ⇒ cần 20 bit
  - `key = (a << 20) | b`
- Hash table open addressing, sentinel `UINT64_MAX` cho ô trống
- Duyệt trạng thái đến khi gặp lại key đã thấy:
  - gặp lại ở index `prev` ⇒ `mu=prev`, `lambda = t-prev`
- Lưu `vals[]` để truy hồi nhanh `S_n` theo công thức nhảy chu kỳ.

### 3.2) Python client

Python làm 3 việc:

1. đọc từng dòng từ socket
2. nếu thấy `Calculate:` ⇒ trả lời ngay
3. nếu thấy block ASCII-art ⇒ OCR ra số
4. khi thấy `Find the value of S_50000000` ⇒ gọi `./s_calc ...` rồi gửi đáp án

Pseudo-flow:

```text
connect
while line = readline():
  if Calculate: send product
  if S_0 / S_1: store
  if VALUE OF C/D/E: read 5 lines, OCR
  if Find S_n: call ./s_calc, send result
```

---

## 4) Notes / Pitfalls

- **Strip `\r`**: nhiều line kết thúc bằng `\r\n`.
- OCR cần robust: nếu ký tự lạ xuất hiện, có thể mặc định là pixel ON và match bằng Hamming distance.
- Không in debug quá nhiều khi chạy thật (stdout chậm có thể góp phần timeout). Khi exploit thật nên hạn chế log.

---

## 5) Kết luận

Bài này là bài **tối ưu thời gian**:

- parse nhanh,
- OCR digit 3×5,
- nhận ra recurrence mod `E` ⇒ state hữu hạn ⇒ có chu kỳ,
- dùng C để tính đủ nhanh dưới 1 giây.

Flag:

```
IIITL{C_15_41w4y5_f4573r_7h4n_py7h0n_5ad6363ca76d}
```
