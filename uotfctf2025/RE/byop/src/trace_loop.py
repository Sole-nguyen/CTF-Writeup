"""
Manual trace of loop bytecode
"""

code_bytes = [
    # PC 0-2: LOADG r0, global['caps']
    0x02, 0x00, 0x00,
    
    # PC 3-6: GETPROP r1, r0.c
    0x20, 0x01, 0x00, 0x03,
    
    # PC 7-10: JMPT r10, +5
    0x61, 0x0a, 0x05, 0x00,  # Jump forward 5 bytes if r10 is truthy
    
    # PC 11-13: SORT r1, key=10
    0x70, 0x01, 0x0a,
    
    # PC 14-17: ADD r10, r0, r0
    0x40, 0x0a, 0x00, 0x00,
    
    # PC 18-22: GETPROPC r2, r3, r1, key=10
    0x21, 0x02, 0x03, 0x01, 0x0a,
    
    # PC 23-26: JMPT r10, +7
    0x61, 0x0a, 0x07, 0x00,  # Jump forward 7 bytes if r10 is set
    
    # PC 27-29: JMP back to PC 7
    # offset = 7 - (27 + 3) = 7 - 30 = -23 = 0xFFE9
    0x60, 0xE9, 0xFF,
    
    # PC 30-32: LOADK r6, const[1]
    0x01, 0x06, 0x01,
    
    # PC 33-38: CALL r7, r2.call(r3, [r6])
    0x30, 0x07, 0x02, 0x03, 0x01, 0x06,
    
    # PC 39-40: RET r7
    0x31, 0x07,
]

print("Iteration 1:")
print("-" * 70)
print("PC 0-2: LOADG - r0 = F9")
print("PC 3-6: GETPROP - r1 = F7")
print("PC 7-10: JMPT r10, +5")
print("  r10 = undefined (falsy) -> don't jump, continue")
print("PC 11-13: SORT r1.e")
print("  F5 reordered, version stays 0")
print("PC 14-17: ADD r10, r0, r0")
print("  r10 = F9 + F9 (becomes NaN or object, truthy!)")
print("PC 18-22: GETPROPC r2, r3, r1.e")
print("  Cache MISS, creates cache entry")
print("  r2 = F1, r3 = F7")
print("PC 23-26: JMPT r10, +7")
print("  r10 = truthy -> jump to PC 30")
print("PC 30-32: LOADK r6, '/flag.txt'")
print("PC 33-38: CALL r7, r2(r6)")
print("  r7 = F1('/flag.txt') - returns '' (absolute path rejected)")
print("PC 39-40: RET r7")
print("  Return '' (empty string)")
print()

print("PROBLEM: We only execute GETPROPC once!")
print("We need to execute it TWICE with different r10 values.")
print()
print("The logic should be:")
print("1. First: GETPROPC (creates cache)")
print("2. Then: SORT")
print("3. Then: Jump back to GETPROPC (uses cache)")
print()
print("Let me redesign...")
