# Ancient_Mystery writeup

The file `secret_message.txt` is base64-encoded repeatedly.

The story hints at:
- every **64 years** re-encoding
- spanning **3136 years**

So the expected number of layers is `3136 / 64 = 49`.

Decoding the ciphertext repeatedly gives:

`flag{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}`

The challenge note says to submit in `kashiCTF{...}` format, so final submit flag is:

`kashiCTF{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}`

## Solver

This is solve.py:
```python 
#!/usr/bin/env python3
import base64
from pathlib import Path


def normalize_flag(s: str) -> str:
    if s.startswith("flag{") and s.endswith("}"):
        return "kashiCTF{" + s[5:]
    return s


def looks_like_base64(data: bytes) -> bool:
    if not data or len(data) % 4 != 0:
        return False
    alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r"
    return all(c in alphabet for c in data)


def main() -> None:
    enc = Path("secret_message.txt").read_bytes().strip()

    rounds = 0
    cur = enc
    while looks_like_base64(cur):
        try:
            nxt = base64.b64decode(cur, validate=True)
        except Exception:
            break
        cur = nxt
        rounds += 1
        if b"flag{" in cur or b"kashiCTF{" in cur:
            break

    raw = cur.decode("utf-8", errors="replace").strip()
    print(f"decode_rounds = {rounds}")
    print(f"raw_flag      = {raw}")
    print(f"submit_flag   = {normalize_flag(raw)}")


if __name__ == "__main__":
    main()
```