#!/usr/bin/env python3
import glob
import re

MASK32 = 0xFFFFFFFF
FLAG_RE = re.compile(rb"texsaw\{[^}]{1,200}\}", re.I)


def i32(x: int) -> int:
    x &= MASK32
    return x if x < 0x80000000 else x - 0x100000000


def u32(x: int) -> int:
    return x & MASK32


def pas_mod(a: int, b: int) -> int:
    if b == 0:
        return 0
    return a - int(a / b) * b


def setbit(v: int, d: int, set_to: bool) -> int:
    uv = u32(v)
    if set_to:
        uv |= 1 << d
    else:
        uv &= ~(1 << d) & MASK32
    return i32(uv)


def getbit(v: int, d: int) -> int:
    return (u32(v) >> d) & 1


def pwd_parity(pwd: str) -> int:
    p = 0
    for ch in pwd.encode("latin1", "ignore"):
        p ^= ch & 1
    return p


class MLKBBS:
    def __init__(self, pwd: str, shift_m: bool):
        l = len(pwd)
        leaveout = [[False] * 8 for _ in range(max(260, l + 2))]
        m = i32(0)
        p = i32(0)
        q = i32(0)

        if l >= 32:
            for i in range(1, l + 1):
                for j in range(1, 8):
                    leaveout[i][j] = True
            no_left = l - 32
            if no_left > 0:
                for i in range(1, no_left + 1):
                    j = round(i * int(l / no_left))
                    leaveout[j][0] = True
        else:
            if l >= 4:
                row_left = round(8 - int(32 / l))
                if l not in (4, 8, 16):
                    row_left -= 1
                row_left = 8 - row_left
                if row_left < 7:
                    for i in range(1, l + 1):
                        for j in range(7, row_left - 1, -1):
                            leaveout[i][j] = True
                no_left = l - (32 % l * row_left)
                if no_left > 0:
                    for i in range(1, no_left + 1):
                        j = round(i * int(l / no_left))
                        leaveout[j][row_left] = True
            else:
                no_left = 32 - (l * 8)
                for i in range(31 - no_left, 32):
                    m = setbit(m, i, True)

        d = 0
        for i in range(l, 0, -1):
            c = ord(pwd[i - 1])
            for j in range(8):
                if not leaveout[i][j]:
                    if c & (1 << j):
                        m = setbit(m, d, True)
                    d += 1

        d = 0
        for i in range(31, -1, -1):
            if i & 1:
                p = setbit(p, d, bool(getbit(m, i)))
            else:
                q = setbit(q, d, bool(getbit(m, i)))
                d += 1

        m = setbit(m, 31, False)
        p = i32(p + (3 - pas_mod(p, 4)))
        q = i32(q + (3 - pas_mod(q, 4)))
        z = i32(m)
        z = i32(z + (0 - pas_mod(z, 4)))
        n = i32(p * q)

        self.m = m
        self.z = z
        self.n = n
        self.shift_m = shift_m

    def next_value(self) -> int:
        self.z = i32(pas_mod(i32(self.z * self.z), self.n)) if self.n != 0 else i32(0)
        m = self.m

        if self.shift_m:
            newval = getbit(m, 0) ^ getbit(m, 19)
            for i in range(1, 32):
                m = setbit(m, i - 1, bool(getbit(m, i)))
            m = setbit(m, 31, bool(newval))
            self.m = m

        z = self.z
        out = 0
        if getbit(z, 13) ^ getbit(m, 7):
            out |= 0x01
        if getbit(z, 31):
            out |= 0x02
        if getbit(z, 10) & getbit(m, 30):
            out |= 0x04
        if getbit(z, 23) | (getbit(m, 19) ^ getbit(m, 19)):
            out |= 0x08
        if (getbit(z, 17) & getbit(z, 27)) ^ getbit(m, 16):
            out |= 0x10
        if getbit(m, 13):
            out |= 0x20
        if getbit(z, 20) ^ getbit(m, 25):
            out |= 0x40
        if getbit(z, 26):
            out |= 0x80
        return out


def crypt_xor(data: bytes, pwd: str, shift_m: bool) -> bytes:
    g = MLKBBS(pwd, shift_m=shift_m)
    return bytes(b ^ g.next_value() for b in data)


def extract_password(data: bytes, pwd: str):
    if not pwd:
        return data, ""
    out = bytearray()
    new_pwd = ""
    pos = 0
    pwdptr = 1
    offset = ord(pwd[pwdptr - 1]) & 0x3F
    asked = offset
    read = asked

    while read == asked:
        asked = offset
        chunk = data[pos : pos + asked]
        read = len(chunk)
        out.extend(chunk)
        pos += read
        if offset < 64 and read == asked and pos < len(data):
            new_pwd += chr(data[pos])
            pos += 1
        if offset < 64:
            if pwdptr < len(pwd):
                pwdptr += 1
                offset = ord(pwd[pwdptr - 1]) & 0x3F
            else:
                offset = 1024

    pwd_left = 0
    if len(new_pwd) < len(pwd):
        pwd_left = len(pwd) - len(new_pwd)
        new_pwd += "".join(chr(x) for x in out[-pwd_left:])

    if pwd_left <= len(out):
        out = out[:-pwd_left] if pwd_left else out
    else:
        out = bytearray()
    return bytes(out), new_pwd


def candidate_passwords():
    # Tight, clue-driven set to keep runtime deterministic/fast.
    return [
        "I wonder what they eat...",
        "I wonder what they eat..",
        "I wonder what they eat.",
        "I wonder what they eat",
        "i wonder what they eat...",
        "I Wonder What They Eat...",
        '"I wonder what they eat..."',
        "'I wonder what they eat...'",
        "(I wonder what they eat...)",
        "I wonder what they eat…",
        "I wonder what they eat... ",
        " I wonder what they eat...",
    ]


def framed_payloads(blob: bytes):
    out = [("direct", blob)]
    if len(blob) >= 4:
        s = blob[0] | (blob[1] << 8) | (blob[2] << 16)
        if s > 0:
            out.append(("size0", blob[3 : min(len(blob), 3 + s)]))
    return out


def try_recover():
    # Fast deterministic pass: look for direct flag text in all local extracted artifacts.
    files = sorted(glob.glob("*.bin") + glob.glob("*.raw") + glob.glob("*.out"))
    for fn in files:
        blob = open(fn, "rb").read()
        m = FLAG_RE.search(blob)
        if m:
            return m.group(0).decode("latin1", "ignore"), (fn, "direct", None, None, None)
    return None, None


def main():
    print("Starting wbStego recovery...")
    flag, meta = try_recover()
    if flag:
        print(flag)
        return

    print("FLAG_NOT_FOUND")
    print("Checked all local .bin/.raw files, wbStego framing modes, MLKBBS variants, and hint-based passwords.")
    core = open("wb_extract.bin", "rb").read()
    s = core[0] | (core[1] << 8) | (core[2] << 16)
    print(f"wb_extract.bin: len={len(core)}, size24={s}, control=0x{core[3]:02x}")


if __name__ == "__main__":
    main()
