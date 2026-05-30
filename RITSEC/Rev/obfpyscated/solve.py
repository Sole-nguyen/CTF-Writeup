#!/usr/bin/env python3
import ast
import io
import marshal
import urllib.request
from pathlib import Path

from Crypto.Cipher import AES
from PIL import Image


def xor_bytes(data: bytes, key: int) -> bytes:
    return bytes(b ^ key for b in data)


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        return resp.read()


def decode_first_stage() -> object:
    text = Path(__file__).with_name("meow.py").read_text()
    mod = ast.parse(text)
    blob = next(node.s for node in ast.walk(mod) if isinstance(node, ast.Bytes))
    stage1 = "".join(chr(b ^ 2) for b in blob)
    mod2 = ast.parse(stage1)
    payload = next(
        node.s for node in ast.walk(mod2) if isinstance(node, ast.Bytes) and len(node.s) > 100
    )
    data = bytes(b ^ 27 for b in payload)
    return marshal.loads(data)


def decode_stage1_params(code) -> tuple[str, bytes, bytes]:
    bytes_consts = [c for c in code.co_consts if isinstance(c, (bytes, bytearray))]
    host_bytes = next(b for b in bytes_consts if len(b) == 15)
    req_bytes = next(b for b in bytes_consts if len(b) > 60)
    key_bytes = next(b for b in bytes_consts if len(b) == 32)
    host = xor_bytes(host_bytes, 42).decode()
    request = xor_bytes(req_bytes, 84)
    key = xor_bytes(key_bytes, 55)
    return host, request, key


def url_from_request(host: str, request: bytes) -> str:
    path = request.split(b" ")[1].decode()
    return f"https://{host}{path}"


def decode_stage2(code, host: str) -> str:
    bytes_consts = [c for c in code.co_consts if isinstance(c, (bytes, bytearray))]
    req_bytes = next(b for b in bytes_consts if len(b) > 60)
    request = xor_bytes(req_bytes, 67)
    url = url_from_request(host, request)
    img_bytes = fetch(url)
    img = Image.open(io.BytesIO(img_bytes))

    coords = next(
        c
        for c in code.co_consts
        if isinstance(c, tuple)
        and c
        and isinstance(c[0], tuple)
        and len(c[0]) == 2
    )
    chars = []
    for x, y in coords:
        r, g, b = img.getpixel((x, y))
        chars.append(chr(r ^ g ^ b))
    return "".join(chars)


def main() -> None:
    stage1 = decode_first_stage()
    host, request, key = decode_stage1_params(stage1)
    url = url_from_request(host, request)
    data = fetch(url)
    nonce = data[-16:]
    tag = data[-32:-16]
    ciphertext = data[:-32]
    plain = AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ciphertext, tag)
    stage2 = marshal.loads(plain)
    flag = decode_stage2(stage2, host)
    print(flag)


if __name__ == "__main__":
    main()
