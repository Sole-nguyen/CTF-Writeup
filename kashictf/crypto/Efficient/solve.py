#!/usr/bin/env python3
import base64
import math
import re
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def parse_output(text: str):
    n = int(re.search(r"n\s*=\s*0x([0-9a-f]+)", text).group(1), 16)
    e = int(re.search(r"e\s*=\s*([0-9]+)", text).group(1))
    ct = int.from_bytes(base64.b64decode(re.search(r"ct\s*=\s*([A-Za-z0-9+/=]+)", text).group(1)), "big")
    iv = base64.b64decode(re.search(r"iv\s*=\s*([A-Za-z0-9+/=]+)", text).group(1))
    flag_ct = base64.b64decode(re.search(r"flag_ct\s*=\s*([A-Za-z0-9+/=]+)", text).group(1))
    return n, e, ct, iv, flag_ct


def main() -> None:
    output_file = next(Path(".").glob("output.txt*"))
    text = output_file.read_text()
    n, e, ct, iv, flag_ct = parse_output(text)

    # Vulnerability: keygen made n = p^2, so factoring is trivial: p = sqrt(n).
    p = math.isqrt(n)
    if p * p != n:
        raise ValueError("n is not a perfect square in this instance.")

    # For n = p^2, phi(n) = p * (p - 1)
    phi = p * (p - 1)
    d = pow(e, -1, phi)

    # RSA decrypt gives the AES key bytes directly.
    key_int = pow(ct, d, n)
    key = key_int.to_bytes((n.bit_length() + 7) // 8, "big").lstrip(b"\x00")
    if len(key) != 16:
        raise ValueError(f"Unexpected AES key length: {len(key)}")

    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(flag_ct)
    flag = unpad(pt, 16).decode()
    print(flag)


if __name__ == "__main__":
    main()
