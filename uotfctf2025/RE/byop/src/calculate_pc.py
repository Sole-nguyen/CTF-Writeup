"""
Calculate actual PC values in bytecode
"""

code = b""

# After header, code starts at offset 0 in bytecode section
pc = 0

# 1. LOADG r0, global["caps"]
print(f"PC {pc}: LOADG r0, global['caps']")
code += bytes([0x02, 0x00, 0x00])
pc += 3

# 2. GETPROP r1, r0.c
print(f"PC {pc}: GETPROP r1, r0.c")
code += bytes([0x20, 0x01, 0x00, 0x03])
pc += 4

# 3. GETPROPC r2, PC, r1, key=10
print(f"PC {pc}: GETPROPC r2, r1.e  (PC value in opcode = {pc+1})")
code += bytes([0x21, 0x02, pc+1, 0x01, 0x0a])
pc += 5

# 4. SORT r1, key=10
print(f"PC {pc}: SORT r1.e")
code += bytes([0x70, 0x01, 0x0a])
pc += 3

# 5. GETPROPC r3, PC, r1, key=10
print(f"PC {pc}: GETPROPC r3, r1.e  (PC value in opcode = {pc+1})")
code += bytes([0x21, 0x03, pc+1, 0x01, 0x0a])
pc += 5

print()
print("Issue: PC values are 7 and 15 (different!)")
print("Cache is stored per PC, so they don't collide.")
print()
print("Solution: We need to:")
print("1. Create cache at some PC")
print("2. SORT")
print("3. Use SAME PC again")
print()
print("But we can't jump backwards easily...")
print("Unless... we use a loop or jump instruction!")
print()
print("Alternative: Create cache, SORT, then use cached index directly")
print("The cache stores the STORAGE INDEX (si), which after SORT points to wrong value")
print()
print("Wait, let me check if there's another way...")
print("If cache hits, it does: holder.sl[cached_si]")
print("After SORT: F5.sl = [F0, F1] (reordered)")
print("Cached si = 0")
print("So holder.sl[0] = F0  <- This IS what we want!")
print()
print("So the exploit SHOULD work if we reuse the same PC!")
print("Let me design bytecode with a jump...")
