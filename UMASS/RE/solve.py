#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile


BATCAVE_DEFAULT = Path(__file__).resolve().parent / "Batcave_Bitflips" / "batcave_license_checker"
LEGO_APK_DEFAULT = Path(__file__).resolve().parent / "Lego_Clicker" / "LegoClicker_umass.apk"


def _read_file(path: Path) -> bytes:
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    return path.read_bytes()


def _extract_legocore_from_apk(apk_path: Path) -> bytes:
    if not apk_path.exists():
        raise SystemExit(f"APK not found: {apk_path}")
    with zipfile.ZipFile(apk_path, "r") as zf:
        for name in (
            "lib/x86_64/liblegocore.so",
            "lib/arm64-v8a/liblegocore.so",
            "lib/x86/liblegocore.so",
            "lib/armeabi-v7a/liblegocore.so",
        ):
            try:
                return zf.read(name)
            except KeyError:
                continue
    raise SystemExit("Could not find liblegocore.so inside the APK")


def solve_batcave(binary_path: Path) -> str:
    data = _read_file(binary_path)
    license_key = b"!_batman-robin-alfred_((67||67))"
    key_off = data.find(license_key)
    if key_off == -1:
        raise SystemExit("Could not locate license key in batcave binary")

    expected = data[key_off + 0x20 : key_off + 0x40]
    flag_enc = data[key_off + 0x40 : key_off + 0x60]
    if len(expected) != 32 or len(flag_enc) != 32:
        raise SystemExit("Unexpected batcave data layout")

    flag = bytes(flag_enc[i] ^ expected[i] for i in range(32))
    flag_str = flag.decode("ascii").rstrip("\x00")
    if not (flag_str.startswith("UMASS{") and flag_str.endswith("}")):
        raise SystemExit("Batcave flag sanity check failed")
    return flag_str


def _u64_le(value: int) -> bytes:
    return value.to_bytes(8, "little")


def solve_lego(lib_bytes: bytes) -> str:
    def pick(addr: int, length: int) -> bytes:
        if addr + length > len(lib_bytes):
            raise SystemExit("Unexpected liblegocore.so layout for this architecture")
        return lib_bytes[addr : addr + length]

    # Tables used by the native syncBrickCache generator (x86_64 build).
    t0 = pick(0x13CDC, 16)
    t1 = pick(0x13DC6, 16)
    t2 = pick(0x13DD4, 16)

    tab_58560 = _u64_le(0x04715D2B883F1A6C)
    tab_58568 = _u64_le(0x39B24E9511C36720)
    tab_58570 = _u64_le(0x9C6428DE417F0A53)
    tab_585F0 = bytes(4)  # Computed to zero in JNI_OnLoad

    def f20310(n: int) -> int:
        q = (n * 0xAAAAAAAB) >> 33  # floor(n/3) for 32-bit n
        r = n - q * 3
        table = t0 if r == 0 else (t1 if r == 1 else t2)
        return table[q]

    def f204e0(val: int, idx: int) -> int:
        t = tab_58570[(idx + 1) & 7]
        return val ^ t

    def f20510(val: int, idx: int) -> int:
        t = tab_58570[idx & 7]
        return (val - t) & 0xFF

    def f20530(val: int, idx: int) -> int:
        t = tab_58568[idx & 7]
        return val ^ t

    def f20560(val: int) -> int:
        return ((val >> 3) | ((val << 5) & 0xFF)) & 0xFF

    def f20580(val: int, idx: int) -> int:
        t = tab_58560[idx & 7]
        return val ^ t

    out = bytearray()
    for i in range(0x29):
        b0 = f20310(i)
        b1 = f204e0(b0, i)
        b2 = f20510(b1, i)
        b3 = f20530(b2, i)
        b4 = f20560(b3)
        b5 = f20580(b4, i)
        b6 = b5 ^ tab_585F0[i & 3]
        out.append(b6)

    flag_str = out.decode("ascii")
    if not (flag_str.startswith("UMASS{") and flag_str.endswith("}")):
        raise SystemExit("Lego flag sanity check failed")
    return flag_str


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve UMASS RE challenges")
    parser.add_argument("--batcave", type=Path, default=BATCAVE_DEFAULT, help="Path to batcave_license_checker")
    parser.add_argument("--lego-apk", type=Path, default=LEGO_APK_DEFAULT, help="Path to LegoClicker_umass.apk")
    parser.add_argument("--lego-lib", type=Path, default=None, help="Path to liblegocore.so (overrides APK)")
    args = parser.parse_args()

    batcave_flag = solve_batcave(args.batcave)
    if args.lego_lib:
        lego_bytes = _read_file(args.lego_lib)
    else:
        lego_bytes = _extract_legocore_from_apk(args.lego_apk)
    lego_flag = solve_lego(lego_bytes)

    print(f"[Batcave] {batcave_flag}")
    print(f"[Lego]    {lego_flag}")


if __name__ == "__main__":
    main()
