# Grawlix / “CALVINBALL STREAM (ADAPTIVE)” — Writeup

**Flag format:** `IIITL{...}`

## 1) Đề bài
Kết nối:

```bash
nc 34.131.216.230 1339
```

Server in ra một “stream” thao tác rất lớn (tới ~100MB ký tự), yêu cầu ta tính giá trị cuối cùng của biến `V` sau khi áp dụng toàn bộ thao tác rồi nhập kết quả.

Điểm mấu chốt nằm ở câu:

> The 2-second timer starts ONLY after the stream is fully delivered.

Tức là **không phải** bạn chỉ có 2 giây từ lúc connect, mà là 2 giây **sau khi server gửi xong 100MB**. Nếu bạn đợi nhận xong rồi mới bắt đầu tính (hoặc copy/paste), gần như chắc chắn trễ.

## 2) Giao thức & luật tính
Banner kiểu:

```
Starting Value (V) = 8594
All operations (except bitwise) are modulo 1000000007.
...
[INCOMING STREAM]
&%$&#@$&@##%%$$@$$$$
```

Các toán tử:

- `@` : `V = V + 101` (mod `1e9+7`)
- `#` : `V = V * 3` (mod `1e9+7`)
- `$` : `V = V ^ 4242` (**XOR bitwise**, **không mod**)
- `%` : nếu `V` chẵn ⇒ `V = V / 2`, lẻ ⇒ `V = (V * 3) + 1` (đề nói “except bitwise are modulo”, nên coi đây là modulo `1e9+7` sau phép tính; chia 2 là chia nguyên)
- `&` : `V = (~V) & 0xFFFFF` (**NOT bitwise**, mask 20-bit)

Lưu ý quan trọng:

- Các phép **bitwise (`$`, `&`)** làm trên integer trực tiếp; riêng `&` còn **mask về 20 bit**.
- Các phép còn lại làm modulo `1000000007`.

## 3) Bẫy / khó khăn
### 3.1) Output cực lớn
Nếu dùng `nc` thuần, bạn sẽ thấy hàng trăm MB ký tự. Tìm flag trong output không giải quyết được vì flag chỉ xuất hiện sau khi bạn trả lời đúng.

### 3.2) Timing
Nếu bạn:
1) nhận xong toàn bộ stream
2) mới bắt đầu tính

thì “2-second timer” sẽ giết bạn. Cách đúng là **vừa nhận vừa tính** (stream-processing).

## 4) Ý tưởng giải
Viết client TCP (C/Python/Go đều được), làm 3 việc:

1. Parse dòng `Starting Value (V) = ...` để lấy `V0`.
2. Đợi marker `[INCOMING STREAM]`, sau đó:
3. Khi stream bắt đầu, với **mỗi byte nhận được**:
   - nếu là một trong `@ # $ % &` thì cập nhật `V` ngay
   - khi gặp `\n` kết thúc stream ⇒ lập tức `send()` kết quả `V` + newline
4. In phần response còn lại (thường chứa `ACCEPTED` + flag).

Độ phức tạp:
- Thời gian: `O(n)` với `n ≈ 100MB` thao tác
- Bộ nhớ: `O(1)` (không cần lưu cả stream)

## 5) Triển khai (C, nhanh & ổn định)
Mình dùng C để đảm bảo tốc độ và không bị overhead khi xử lý 100MB trong 2 giây sau khi stream kết thúc.

### 5.1) Những điểm cần đúng
- Parse header theo line để bắt `Starting Value`.
- Chuyển mode sang xử lý stream ngay sau `[INCOMING STREAM]`.
- Trong mode stream: gặp `\n` thì dừng xử lý stream và gửi kết quả.
- Với `&`: `V = (~V) & 0xFFFFF`.
- Với `$`: `V ^= 4242`.
- Với phép modulo: giữ `V` trong `uint64_t`, mod `1e9+7` khi cần.

### 5.2) Code
File solver đã dùng:

- `solve.c`: client TCP + stream-processing

Bạn có thể xem trực tiếp code trong repo (cùng thư mục với writeup này).

Compile:

```bash
gcc -O3 -march=native -pipe -std=c11 -Wall -Wextra -o solve solve.c
```

Chạy:

```bash
./solve
```

## 6) Kết quả
Chạy solver sẽ in ra phản hồi server, ví dụ:

```
ACCEPTED. You are a data-processing god.

Congratulations! IIITL{C4lv1nb4ll_57r34m_0v3r104d_8762_n0_5l33p_bac9cac70848}
```

**Flag:**

```
IIITL{C4lv1nb4ll_57r34m_0v3r104d_8762_n0_5l33p_bac9cac70848}
```

## 7) Ghi chú thêm
- Tổng thời gian chạy có thể ~10–20s vì bạn phải **download** 100MB từ server. Điều quan trọng là **khi vừa download vừa tính**, nên đến cuối stream bạn trả lời gần như ngay lập tức (không sợ timer 2s).
- Python vẫn có thể làm được nếu tối ưu tốt (đọc chunk bytes, dùng bảng dispatch), nhưng C là lựa chọn an toàn nhất cho dạng challenge “stream overload”.
