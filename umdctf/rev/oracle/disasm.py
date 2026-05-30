
import struct
import capstone

with open('oracle','rb') as f:
    data = f.read()

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

# Disassemble .text section
text_off = 0x11c0
text_size = 0x3149
text = data[text_off:text_off+text_size]
base_va = 0x11c0  # virtual address

print('=== .text section disassembly ===')
for instr in md.disasm(text, base_va):
    print(f'  {hex(instr.address)}: {instr.mnemonic} {instr.op_str}')

print()

# Disassemble chk section
chk_off = 0x4340
chk_size = 0x23e
chk = data[chk_off:chk_off+chk_size]

print('=== chk section disassembly ===')
for instr in md.disasm(chk, 0x4340):
    print(f'  {hex(instr.address)}: {instr.mnemonic} {instr.op_str}')
