#!/usr/bin/env python3
"""
UMDCTF - roulette (rev)
Flag: UMDCTF{I_R3ALLY-want-to-pl4y-the-p0werball,+but-my-d4d-said-no-so-im-b3tting-ill-win-on-POLYMARKETinstead}

Binary verifier chia input 106 bytes thành 27 chunk (26×4 bytes LE + 1×2 bytes),
rồi so sánh mỗi chunk với hằng số hardcoded bên trong. Không có crypto - chỉ cần
dump giá trị kỳ vọng từng vòng là ra flag.
"""

import subprocess
from pathlib import Path

# Giá trị u32 kỳ vọng của từng chunk (dump từ IDA/GDB tại mỗi vòng so sánh).
# Vòng 0-25: chunk 4 bytes little-endian  → input[4*i : 4*i+4]
# Vòng 26  : chunk 2 bytes little-endian  → input[104:106]
REQUIRED_CHUNKS = [
    1128549717, 1232815700, 1093882463,  760826956, 1953390967,  762278957, 2033478768,
    1701344301, 1999663149, 1633841765,  724331628,  762606946, 1680701805, 1932354612,
     761555297, 1932357486, 1835609455, 1949524525, 1735289204, 1819044141, 1852405549,
     762212141, 1498173264, 1263681869, 1852396613, 1634038899,      32100,
]


def build_payload() -> bytes:
    """Ghép các chunk thành 106 bytes payload."""
    out = b""
    for i, v in enumerate(REQUIRED_CHUNKS):
        if i < 26:
            out += v.to_bytes(4, "little")
        else:                                    # vòng cuối chỉ 2 bytes
            out += (v & 0xFFFF).to_bytes(2, "little")
    return out


def decode_flag(payload: bytes) -> str:
    return payload.decode("ascii")


def main() -> None:
    payload = build_payload()
    flag = decode_flag(payload)

    print("[*] Payload length : %d bytes" % len(payload))
    print("[*] Flag           : %s" % flag)
    print()

    # Chạy binary (Linux ELF - cần WSL hoặc môi trường Linux)
    chall = Path(__file__).with_name("roulette")
    if not chall.exists():
        print("[!] Binary 'roulette' not found, skipping execution.")
        return

    print("[*] Running binary (requires Linux/WSL)...")
    try:
        result = subprocess.run(
            [str(chall)],
            input=payload + b"\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        print(result.stdout.decode("latin-1", "replace"))
        if result.returncode != 0:
            print("[!] Exit code: %d" % result.returncode)
    except OSError as e:
        print("[!] Cannot execute binary on this OS: %s" % e)
        print("[*] Run on Linux/WSL: python3 solve.py")


if __name__ == "__main__":
    main()
