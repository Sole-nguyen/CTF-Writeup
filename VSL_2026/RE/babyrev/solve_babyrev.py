def rol(val, shift):
    """Rotate Left 32-bit integer."""
    return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

# Encrypted bytes from .rodata (unk_20E0)
target = [
    0x25, 0x5F, 0x2D, 0x51, 0x5B, 0x34, 0x52, 0x5A, 0x6F, 0x87, 0xEA, 0x67, 0x56, 0x48, 0x41, 0xAB, 
    0xA5, 0x76, 0x3C, 0x23, 0x1F, 0x27, 0xB9, 0xC1, 0xEB, 0xF0, 0x75, 0xE3, 0x35, 0x2B, 0x20, 0x3A, 
    0xF4, 0x2D, 0xB2, 0x9B, 0x8F, 0x13, 0x2B, 0xDB, 0xBD, 0x77, 0x3A, 0xA8, 0xF4, 0x82, 0xB3, 0xA9, 
    0xFB, 0x7C, 0x5E, 0x66, 0xB5, 0x84, 0xFA
]

# Initial State Constants from Disassembly
r9 = 0x45D9F3B
esi = 0xC0FEFEA1
r10 = 0
flag_body = []

print("Brute-forcing flag characters...")

# Loop 55 times (length of the inner flag)
for i in range(55):
    # Calculate the permuted index where the result is stored
    # Logic derived from: mov rax, r8; imul r14 (magic div 55) ...
    target_idx = (i * 7) % 55
    goal_byte = target[target_idx]
    
    char_found = False
    
    # Try every printable ASCII character
    for c in range(32, 127): 
        # --- Simulation of loc_1380 logic ---
        
        # 1. Add rolling key r9
        val = (c + r9) & 0xFFFFFFFF
        
        # 2. Update ESI state
        temp_esi = (esi ^ val) & 0xFFFFFFFF
        
        # 3. Rotate Left
        # Shift amount logic: derived from reciprocal multiplication by 13
        shift = (i % 13) + 1
        temp_esi = rol(temp_esi, shift)
        
        # 4. Subtract constant
        temp_esi = (temp_esi - 0x61C88E4F) & 0xFFFFFFFF
        
        # 5. Calculate the output byte (dl)
        # Logic: xor various shifted terms and products
        term1 = temp_esi >> 17
        term2 = temp_esi >> 3
        term3 = (c * (i + 2)) & 0xFFFFFFFF # imul eax, ebx
        
        # Combined XORs
        res = (term1 ^ term2 ^ term3 ^ r10 ^ 0x5B) & 0xFF
        
        # Check if it matches the target
        if res == goal_byte:
            flag_body.append(chr(c))
            
            # Commit state updates for the next iteration
            r9 = (r9 + 0x45D9F3B) & 0xFFFFFFFF
            esi = temp_esi
            r10 = (r10 + 11) & 0xFFFFFFFF
            
            char_found = True
            break
    
    if not char_found:
        print(f"Failed to find char at index {i}")
        break

final_flag = "VSL{" + "".join(flag_body) + "}"
print(f"\nFlag Found: {final_flag}")