#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path

FLAG_RE = re.compile(r"kashiCTF\{[^}\r\n]*\}")


def default_pcap_path() -> str:
    matches = sorted(Path(".").glob("ttl_stego.pcap*"))
    if not matches:
        raise FileNotFoundError("No file matching 'ttl_stego.pcap*' was found.")
    return str(matches[0])


def read_ttls(pcap_path: str) -> list[int]:
    cmd = ["tshark", "-r", pcap_path, "-T", "fields", "-e", "ip.ttl"]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise RuntimeError("tshark is required but was not found in PATH.")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(exc.stderr.strip() or "Failed to read PCAP with tshark.")

    ttls: list[int] = []
    for line in output.splitlines():
        value = line.strip()
        if not value:
            continue
        ttls.append(int(value))
    return ttls


def bits_to_bytes(bits: list[str], offset: int) -> bytes:
    out = bytearray()
    for i in range(offset, len(bits) - 7, 8):
        out.append(int("".join(bits[i : i + 8]), 2))
    return bytes(out)


def extract_flag(ttls: list[int]) -> str:
    mappings = ({64: "0", 65: "1"}, {64: "1", 65: "0"})
    for mapping in mappings:
        if any(ttl not in mapping for ttl in ttls):
            continue
        bits = [mapping[ttl] for ttl in ttls]
        for offset in range(8):
            candidate = bits_to_bytes(bits, offset).decode("latin1", errors="ignore")
            match = FLAG_RE.search(candidate)
            if match:
                return match.group(0)
    raise RuntimeError("Flag not found in TTL stream.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Recover flag hidden in ICMP TTL values.")
    parser.add_argument("pcap", nargs="?", help="Path to PCAP file (default: ttl_stego.pcap*)")
    args = parser.parse_args()

    pcap_path = args.pcap or default_pcap_path()
    ttls = read_ttls(pcap_path)
    flag = extract_flag(ttls)
    print(flag)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[!] {exc}", file=sys.stderr)
        raise SystemExit(1)
