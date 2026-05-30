#!/usr/bin/env python3
import glob
import io
import re
import struct
import zipfile
import zlib


def parse_png_rgb8(png_bytes: bytes):
    if png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG")

    offset = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()

    while offset + 12 <= len(png_bytes):
        length = struct.unpack(">I", png_bytes[offset : offset + 4])[0]
        ctype = png_bytes[offset + 4 : offset + 8]
        data = png_bytes[offset + 8 : offset + 8 + length]

        if ctype == b"IHDR":
            width, height, bit_depth, color_type, comp, flt, interlace = struct.unpack(
                ">IIBBBBB", data
            )
            if not (bit_depth == 8 and color_type == 2 and comp == 0 and flt == 0 and interlace == 0):
                raise ValueError("Unsupported PNG format")
        elif ctype == b"IDAT":
            idat.extend(data)
        elif ctype == b"IEND":
            break

        offset += 12 + length

    raw = zlib.decompress(bytes(idat))
    bpp = 3
    stride = width * bpp

    out = bytearray(height * stride)
    i = 0
    prev = bytearray(stride)

    for y in range(height):
        f = raw[i]
        i += 1
        row = bytearray(raw[i : i + stride])
        i += stride

        if f == 1:  # Sub
            for x in range(stride):
                row[x] = (row[x] + (row[x - bpp] if x >= bpp else 0)) & 0xFF
        elif f == 2:  # Up
            for x in range(stride):
                row[x] = (row[x] + prev[x]) & 0xFF
        elif f == 3:  # Average
            for x in range(stride):
                row[x] = (row[x] + ((prev[x] + (row[x - bpp] if x >= bpp else 0)) >> 1)) & 0xFF
        elif f == 4:  # Paeth
            for x in range(stride):
                a = row[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                row[x] = (row[x] + pr) & 0xFF

        out[y * stride : (y + 1) * stride] = row
        prev = row

    return width, height, bytes(out)


def iend_end(png_bytes: bytes) -> int:
    if png_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG")
    offset = 8
    while offset + 12 <= len(png_bytes):
        length = struct.unpack(">I", png_bytes[offset : offset + 4])[0]
        ctype = png_bytes[offset + 4 : offset + 8]
        end = offset + 12 + length
        if ctype == b"IEND":
            return end
        offset = end
    raise ValueError("IEND not found")


def bits_to_bytes_msb(bits):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for bit in bits[i : i + 8]:
            b = (b << 1) | bit
        out.append(b)
    return bytes(out)


def main():
    candidates = sorted(glob.glob("Temoc_keyring.png*"))
    if not candidates:
        raise FileNotFoundError("Main PNG artifact not found")

    main_png_path = candidates[0]
    main_png = open(main_png_path, "rb").read()

    tail = main_png[iend_end(main_png) :]
    zf = zipfile.ZipFile(io.BytesIO(tail))

    orig = zf.read("key/Temoc_keyring(orig).png")
    marked = zf.read("key/where_are_my_keys.png")

    w1, h1, p1 = parse_png_rgb8(orig)
    w2, h2, p2 = parse_png_rgb8(marked)
    if (w1, h1) != (w2, h2):
        raise ValueError("Image size mismatch")

    # Hidden bits are carried by LSB differences in the first row, red channel.
    row_width = w1
    bits = [((p1[x * 3] ^ p2[x * 3]) & 1) for x in range(row_width)]
    decoded = bits_to_bytes_msb(bits)

    m = re.search(rb"texsaw\{[^}]+\}", decoded)
    if not m:
        raise ValueError("Flag not found")

    print(m.group(0).decode())


if __name__ == "__main__":
    main()
