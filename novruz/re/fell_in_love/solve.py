#!/usr/bin/env python3

def rc4(data: bytes, key: bytes) -> bytes:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 0xFF
        s[i], s[j] = s[j], s[i]

    i = 0
    j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) & 0xFF
        j = (j + s[i]) & 0xFF
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) & 0xFF]
        out.append(b ^ k)
    return bytes(out)


def main() -> None:
    encrypted_flag = bytes.fromhex(
        "65f945ce8a60e090fe66ff67ef1bd12e"
        "f16ba40f969ebec00b88c34006275ad2"
        "dfa6150d8defcf2983a4443dd79bf49e"
        "87674dcf4e5ae06bf413e1dcbbce7314"
        "ee09e34f46"
    )
    key = b"this_is_not_flag"
    flag = rc4(encrypted_flag, key).decode()
    print(flag)


if __name__ == "__main__":
    main()
