#!/usr/bin/env python3
import base64
import re
import subprocess
import zlib
from pathlib import Path


PCAP_PATH = Path("zip_extracted/firewall-packet-capture.pcap")


def extract_dns_chunks() -> list[str]:
    cmd = [
        "tshark",
        "-n",
        "-r",
        str(PCAP_PATH),
        "-Y",
        'dns.flags.response==0 && ip.src==172.16.0.50 && dns.qry.name contains "domainforhire.aws.jerseyctf.com"',
        "-T",
        "fields",
        "-e",
        "dns.qry.name",
    ]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    chunks = []
    for line in out.splitlines():
        q = line.strip().rstrip(".")
        if not q:
            continue
        chunks.append(q.split(".")[0])
    return chunks


def parse_cab_and_extract_flag(cab_bytes: bytes) -> tuple[str, str]:
    b = bytearray(cab_bytes)
    b[:4] = b"MSCF"

    coff_files = int.from_bytes(b[16:20], "little")
    c_folders = int.from_bytes(b[26:28], "little")
    c_files = int.from_bytes(b[28:30], "little")
    if c_folders != 1 or c_files != 1:
        raise RuntimeError("Unexpected CAB layout")

    coff_cab_start = int.from_bytes(b[36:40], "little")
    c_cfdata = int.from_bytes(b[40:42], "little")

    off = coff_files
    cb_file = int.from_bytes(b[off : off + 4], "little")
    off += 16
    end = b.find(b"\x00", off)
    filename = b[off:end].decode("latin1")

    p = coff_cab_start
    if c_cfdata < 1:
        raise RuntimeError("No CFDATA blocks")
    cb_data = int.from_bytes(b[p + 4 : p + 6], "little")
    comp = bytes(b[p + 8 : p + 8 + cb_data])
    if not comp.startswith(b"CK"):
        raise RuntimeError("Not MSZIP block")

    dec = zlib.decompress(comp[2:], -15)
    if len(dec) != cb_file:
        # still usable; no hard fail
        pass

    m = re.search(rb"jctf\{[^}]+\}", dec, re.I)
    if not m:
        raise RuntimeError("Flag not found in decompressed payload")
    return filename, m.group(0).decode()


def main():
    chunks = extract_dns_chunks()
    b64 = "".join(chunks)
    raw = base64.b64decode(b64)
    filename, flag = parse_cab_and_extract_flag(raw)

    print("[+] DNS chunks:", len(chunks))
    print("[+] Decoded bytes:", len(raw))
    print("[+] Exfiltrated file:", filename)
    print("[+] Flag:", flag)


if __name__ == "__main__":
    main()

