#!/usr/bin/env python3
import base64
import zipfile

DOCX_NAME = "challenge.docx?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MTJ9.acf06g.iWOzLzZsV-9CeSmECLLro7vPlZo"

with zipfile.ZipFile(DOCX_NAME, "r") as zf:
    encoded = zf.read("secret.txt").decode("ascii").strip()

flag = base64.b64decode(encoded).decode("utf-8")
print(flag)
