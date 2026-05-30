# Entropy (Incognito CTF) — Writeup chi tiết

**Flag format:** `IIITL{...}`  
**Kết nối:** `nc 34.131.216.230 1340`

## 1) Mô tả nhanh bài
Khi kết nối tới service, ta thấy một UI dạng “màn hình” cập nhật liên tục và nhận điều khiển kiểu game (W/A/S/D, Q để thoát). Nếu dùng `nc`/terminal bình thường, rất dễ bị **mất ANSI escape** hoặc hiển thị rác, khiến việc đọc trạng thái thật sự khó.

Bản chất: server liên tục render một **lưới (grid)** bằng **ANSI escape sequences** (màu nền 256-color), trong đó:
- Vị trí người chơi (cursor) được vẽ bằng token `><`
- Đích (goal) được vẽ bằng block `▓▓`
- Mỗi ô còn lại hiển thị 2 ký tự hex `00..FF` (không phải dữ liệu flag, chủ yếu là “texture/noise”)

Mục tiêu: điều khiển cursor đi tới goal và lấy flag (server in flag trong output stream).

---

## 2) Reverse engineering giao thức render ANSI
### 2.1. Dấu hiệu bắt đầu frame
Mỗi lần server “vẽ lại màn hình”, nó clear screen bằng ANSI:

- `ESC[2J` (clear screen)
- `ESC[H` (move cursor về home)

Trong bytes, đây là:

```text
\x1b[2J\x1b[H
```

Ta gọi chuỗi này là **CLS marker**. Một “frame” bắt đầu sau CLS marker.

### 2.2. Cách mỗi ô (cell) được vẽ
Quan sát raw bytes cho thấy mỗi cell dùng background color 256-color:

```text
ESC[48;5;<idx>m ... <2 ký tự hiển thị> ESC[0m
```

- `<idx>`: số màu nền (0..255)
- Sau đó có thể có thêm style codes `ESC[...m` (bold, fg, v.v.)
- Nội dung là **2 ký tự hiển thị**:
  - thường là `"AB"` hex
  - hoặc `"><"` (cursor)
  - hoặc `"▓▓"` (goal) — lưu ý đây là Unicode multibyte

Regex parse cell (bytes) dùng trong script:

```python
cell_re = re.compile(
  rb"\x1b\[48;5;(\d+)m(?:\x1b\[[0-9;?]*m)*(.+?)\x1b\[0m"
)
```

> Điểm quan trọng: **không giả định 2 bytes** cho content vì `▓` là UTF-8 multibyte. Ta decode `utf-8` với `errors='ignore'`.

---

## 3) Xác định kích thước lưới và token quan trọng
Khi parse đủ một frame, đếm được tổng số cell ổn định là:

- **51 × 51 = 2601 cells**

Quy ước tọa độ mình dùng:
- `(y, x)` zero-based trong code parse (`0..50`)
- Khi nói “in-game” mình hay dùng 1-based cho dễ nhìn (`1..51`)

Token:
- Cursor: `><`
- Goal: `▓▓`

Hai vị trí thường thấy:
- Cursor khởi đầu rất ổn định tại gần góc trên-trái (thực nghiệm: `(1,1)` theo 1-based)
- Goal gần góc dưới-phải (thực nghiệm: `(49,49)` theo 1-based)

---

## 4) Suy luận luật di chuyển và “tường”
### 4.1. Tường liên quan mạnh tới màu nền
Thử nghiệm thống kê từ cùng một vị trí (start) với việc nhấn sang phải (`d`):
- Nếu **bg < 64** ở ô đích: tỉ lệ move thành công ~ **0%**
- Nếu **bg ≥ 64**: move có thể thành công nhưng **không chắc chắn** (thường ~40–80% tuỳ giai đoạn)

Kết luận: `bg < 64` hoạt động như **wall/closed** trong frame đó.

### 4.2. “Fail move” thường là no-op, nhưng vẫn có reset/teleport
Ở nhiều vị trí, nhấn vào ô bị đóng chỉ làm cursor **đứng yên** (an toàn).
Tuy nhiên trong quá trình solve, có hiện tượng cursor bị **reset** về start hoặc nhảy bất thường khi:
- spam phím quá nhanh
- va vào border / điều kiện đặc biệt
- trạng thái “mở/đóng” thay đổi theo thời gian, làm path tĩnh (đi thẳng xuống rồi đi thẳng phải) dễ bị “kẹt” rồi cuối cùng reset.

Điểm then chốt: ta không thể chỉ dùng một path cố định và spam.

---

## 5) Ý tưởng giải: BFS theo **từng frame** (dynamic maze)
Vì “cage/pattern” thay đổi theo thời gian (màu nền cập nhật), cách bền vững nhất là:

1. Mỗi lần nhận được **frame mới**, build map **open/closed**:
   - `open = (bg >= 64)`
2. Tìm `cur` (cursor) và `goal` trong frame:
   - `cur = vị trí token '><'`
   - `goal = vị trí token '▓▓'` (nếu có; nếu không thấy thì fallback `(49,49)`)
3. Chạy **BFS** trên grid open để tìm đường ngắn nhất từ `cur` tới `goal` ngay trong frame hiện tại.
4. Lấy **bước kế tiếp** trên đường đó và gửi đúng 1 phím (`w/a/s/d`).
5. Nếu bước đó **không di chuyển** (server reject), đọc frame tiếp theo và thử lại (có thể retry vài lần).
6. Trong suốt quá trình, quét raw stream để tìm regex flag:
   - `IIITL\{[^}]+\}`

Điểm mạnh: BFS luôn “hợp thời” với trạng thái tường hiện tại nên tránh đi vào vùng đóng/border gây reset.

---

## 6) Kỹ thuật parse frame ổn định (rất quan trọng)
Pitfall lớn nhất là chia frame theo “2 CLS markers” sẽ lỗi khi tốc độ redraw không đều.

Giải pháp ổn định:
- Dùng state machine:
  1. Chờ thấy CLS
  2. Parse đúng **2601 cells** bằng regex `cell_re`
  3. Khi đủ 2601 cells → đó là 1 frame hoàn chỉnh

Pseudo-code:

```python
while time < deadline:
  recv thêm bytes vào buffer
  nếu chưa vào frame: tìm CLS, cắt buffer
  nếu đang trong frame: chạy regex finditer cho tới khi đủ 2601 matches
  trả về list cells
```

---

## 7) Code tham khảo (solver Python)
Dưới đây là skeleton rút gọn đúng theo cách mình solve (BFS-per-frame + scan flag).

```python
import socket, time, re, collections

HOST, PORT = "34.131.216.230", 1340
CLS = b"\x1b[2J\x1b[H"
W = 51
L = W * W

cell_re = re.compile(
  rb"\x1b\[48;5;(\d+)m(?:\x1b\[[0-9;?]*m)*(.+?)\x1b\[0m"
)
flag_re = re.compile(rb"IIITL\{[^}]+\}")

DIRS = [(-1,0,b"w"),(1,0,b"s"),(0,-1,b"a"),(0,1,b"d")]


def read_frame(sock, buf, in_frame, deadline):
  while time.time() < deadline:
    try:
      d = sock.recv(65536)
      if d:
        buf += d
        m = flag_re.search(buf)
        if m:
          return ("FLAG", m.group(0), buf, in_frame)
    except socket.timeout:
      pass

    if not in_frame:
      a = buf.find(CLS)
      if a == -1:
        continue
      buf = buf[a+len(CLS):]
      in_frame = True

    cells = []
    endpos = None
    for m in cell_re.finditer(buf):
      bg = int(m.group(1))
      ct = m.group(2).decode("utf-8", "ignore")
      cells.append((bg, ct))
      if len(cells) == L:
        endpos = m.end()
        break

    if endpos is None:
      continue

    buf = buf[endpos:]
    in_frame = False
    return ("FRAME", cells, buf, in_frame)

  return (None, None, buf, in_frame)


def find_token(cells, tok):
  for i, (_, ct) in enumerate(cells):
    if ct == tok:
      return divmod(i, W)
  return None


def bfs(openmask, start, goal):
  sy, sx = start
  gy, gx = goal
  sidx = sy*W + sx
  gidx = gy*W + gx
  q = collections.deque([sidx])
  prev = {sidx: None}
  while q:
    idx = q.popleft()
    if idx == gidx:
      return prev
    y, x = divmod(idx, W)
    for dy, dx, _ in DIRS:
      ny, nx = y+dy, x+dx
      if 0 <= ny < W and 0 <= nx < W:
        nidx = ny*W + nx
        if nidx not in prev and openmask[nidx]:
          prev[nidx] = idx
          q.append(nidx)
  return None


def solve():
  s = socket.create_connection((HOST, PORT), timeout=5)
  s.settimeout(0.2)
  buf = b""
  in_frame = False
  deadline = time.time() + 58

  kind, payload, buf, in_frame = read_frame(s, buf, in_frame, deadline)
  if kind == "FLAG":
    print(payload.decode())
    return
  cells = payload

  while time.time() < deadline:
    cur = find_token(cells, "><")
    goal = find_token(cells, "▓▓") or (49, 49)

    openmask = [(bg >= 64) for (bg, _) in cells]
    openmask[cur[0]*W + cur[1]] = True
    openmask[goal[0]*W + goal[1]] = True

    prev = bfs(openmask, cur, goal)
    if not prev:
      # kích hoạt frame mới bằng một phím (tuỳ tình hình)
      s.sendall(b"a")
    else:
      gidx = goal[0]*W + goal[1]
      if gidx not in prev:
        s.sendall(b"a")
      else:
        # truy vết để lấy bước kế tiếp
        path = [gidx]
        while prev[path[-1]] is not None:
          path.append(prev[path[-1]])
        if len(path) < 2:
          pass
        else:
          nxt = path[-2]
          ny, nx = divmod(nxt, W)
          dy, dx = ny-cur[0], nx-cur[1]
          for ddy, ddx, key in DIRS:
            if (ddy, ddx) == (dy, dx):
              s.sendall(key)
              break

    kind, payload, buf, in_frame = read_frame(s, buf, in_frame, deadline)
    if kind == "FLAG":
      print(payload.decode())
      return
    if kind == "FRAME":
      cells = payload

  print("timeout")


if __name__ == "__main__":
  solve()
```

---

## 8) Kết quả
Chạy BFS-per-frame solver (kèm scan flag) sẽ in được:

```
IIITL{K4l31d05c0p3_M4z3_M4573r_9921_n0_3y35_f83bcb3ecc54}
```

---

## 9) Notes/Debug tips
- Nếu dùng `nc` mà thấy “hex rác” hoặc UI bị phá, là do terminal/pipe xử lý ANSI khác nhau. Nên dùng Python socket để lấy raw bytes.
- Luôn parse theo “1 CLS + đủ 2601 cells” để tránh lệch frame.
- Scan flag trên **raw buffer bytes**, đừng chỉ scan nội dung cell.
- Nếu solver bị reset, giảm spam và dựa vào BFS/1-step-per-frame + retry ngắn.
