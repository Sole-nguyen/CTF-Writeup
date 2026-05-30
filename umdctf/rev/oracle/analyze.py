
"""
Oracle CTF Challenge Analysis

Key findings from binary analysis:
1. The binary reads a ticket file from argv[1] (or stdin via fd)  
2. The ticket format: "-----BEGIN MARKET TICKET-----\n<base64>\n-----END MARKET TICKET-----\n"
3. Decoded ticket: TKT\x01 + 4-byte size + N bytes of data

The "chk" section (0x4340) contains:
- A syscall wrapper at 0x4340
- A function at 0x4370 that reads from stdin/tty and validates format
  It looks for: 10 chars matching some key, then a space/tab/newline, then a number

From the main function at 0x11c0:
- Computes a hash (murmur-like) of some data section
- Calls function at 0x4370 (input validation)
- Sets up AES-like key material (128-bit = 4 x 32-bit words)
- Calls mmap (syscall 0xa = mmap) to map memory
- Calls function at 0x2940 (XTEA decrypt feed.bin with the key)
- Then calls function at 0x5220 (main oracle logic)

From function at 0x5220 (the main oracle at VA 0x5220, file offset 0x5220):
Wait - the .xtext section is at 0x5000 VA, but 0x5000 file offset too.
So 0x5220 is within .xtext which is ENCRYPTED!

The key facts:
- The ticket has TKT\x01 + size + payload (32 bytes = SHA-256 HMAC?)
- The feed.bin is encrypted data that gets decrypted
- The oracle verifies the ticket before decrypting/processing the feed

Let me look at the XTEA/TEA cipher at 0x2880:
sum starts at 0, subtracts 0x61c88647 each iteration = XTEA delta in reverse (decryption)
This is XTEA decryption with:
- 32 rounds (sum goes from 0 to 0xc6ef3720 which is delta*32 negated)  
- Actually: sum -= 0x61c88647 each round, ends when sum == 0xc6ef3720
  0xc6ef3720 = -(0x61c88647 * 32) mod 2^32... wait
  Actually 0x9e3779b9 is the normal delta, but 0x61c88647 = 0x9e3779b9 * 0xa (close)
  Let me check: 0x9e3779b9 = 2654435769
  0x61c88647 = 1640531527
  Hmm, 0x9e3779b9 / 2 = 0x4f1bbdcc... not matching
  Actually 0x61c88647 = 0xffffffff - 0x9e3779b8 + 1 = -0x9e3779b9 mod 2^32? No
  0xffffffff - 0x61c88647 + 1 = 0x9e3779b9. Yes! So 0x61c88647 = -0x9e3779b9 mod 2^32
  So each round: sum -= 0x61c88647 = sum += 0x9e3779b9 (the TEA delta!)
  The loop runs until sum == 0xc6ef3720
  0xc6ef3720 = 0x9e3779b9 * 32 mod 2^32 = 3337565497 * 1... let me compute:
  0x9e3779b9 * 32 = 0x13c6ef3720... lower 32 bits = 0xc6ef3720. Yes!
  So this is TEA/XTEA ENCRYPTION! Sum goes from 0 to delta*32.
  
Wait, let me re-read: "sub esi, 0x61c88647" and loops until "cmp esi, 0xc6ef3720"
0xc6ef3720 = what?
In Python: (-0x61c88647 * 32) % (2**32) = (0x9e3779b9 * 32) % (2**32) = 0xc6ef3720
Yes. So sum accumulates 32 times: 0x9e3779b9 * 32 (subtracting -delta = adding delta)
This is TEA ENCRYPTION with 32 rounds.

Key derivation at 0x11c0:
- ebx = 0xc0def1ab (initial murmur hash seed)
- Computes murmur-like hash of some data section  
- After calling 0x4370 (get stdin input), r9d = eax (some flag)
- Then XORs 4 dwords with the hash value ebx and with values from two tables
- If r9d != 0: XOR first dword with 0xdeadbeef
- Then sets up AES key expansion? (pshuflw, pxor with xmm1 from rodata)

The 4 key words are stored at [rsp+0x20..0x2f] (16 bytes)

The key material:
- rdi = table at rip+0x5dc0 (VA: 0x1239+0x5dc0 = 0x6ff9)... wait these are VA
  rip+0x5dc0 from 0x1239: 0x1239+5+0x5dc0 = 0x6ff9 (VA) 
  File offset = 0x6ff9 - 0 (loaded at 0) ... actually PIE load = base 0
  File offset = 0x6ff9 ... within .xtext (0x5000-0x6000)?? No, .xtext is at VA 0x5000-0x6000 in file
  
Actually for a PIE binary with base 0, VA = file offset for sections before .bss.
So 0x6ff9 is a file offset in .xtext? No, .xtext is at 0x5000-0x6000.
Let me recalculate: rip at 0x1239 + 5 = 0x123e, then + 0x5dc0 = 0x6ffe.
.xtext is 0x5000 to 0x5000+0x1000 = 0x6000. So 0x6ffe is past .xtext.
But from section headers: xtext type=1 (PROGBITS) addr=0x5000, off=0x5000, size=0x1000
Then .fini at 0x6000, .rodata at 0x7000.
So VA 0x6ffe is in the .fini/.unnamed region between .xtext and .rodata.
Hmm, 0x6ffe is close to 0x7000 which is .rodata.

Let me be more careful:
lea rdi, [rip + 0x5dc0] at address 0x1239 in the text section
rip = 0x1239 + 5 (instruction length) = 0x123e  -- wait, lea is 7 bytes
Actually `lea rdi, [rip+0x5dc0]` at 0x1239 is 7 bytes: 0x1239+7=0x1240 
So rip = 0x1240, and target = 0x1240 + 0x5dc0 = 0x7000. That's .rodata!

lea r8, [rip+0x5ddf] at 0x122a is 7 bytes: rip=0x1231, target=0x1231+0x5ddf=0x7010

So:
- rdi = 0x7000 (first table in .rodata) 
- r8 = 0x7010 (second table, 16 bytes into .rodata)

From .rodata dump:
0x7000: 78 56 34 12 f0 de bc 9a 98 ba dc fe 21 43 65 87  (4 little-endian dwords: 0x12345678, 0x9abcdef0, 0xfedcba98, 0x87654321)
0x7010: a5 00 06 7a e1 c4 ca b6 cd 64 66 1e b8 d1 9b 23  (key material?)
"""

import struct

with open('oracle', 'rb') as f:
    data = f.read()

# Parse .rodata
rodata_off = 0x7000
rodata_size = 0xa30

print("=== Key Material Analysis ===")
print()

# Table at 0x7000 (rdi)
table1 = data[rodata_off:rodata_off+16]
print("Table1 (dwords xor'd with hash):")
for i in range(4):
    val = struct.unpack_from('<I', table1, i*4)[0]
    print(f"  [{i}] = 0x{val:08x}")

# Table at 0x7010 (r8)
table2 = data[rodata_off+0x10:rodata_off+0x20]
print("\nTable2 (dwords xor'd):")
for i in range(4):
    val = struct.unpack_from('<I', table2, i*4)[0]
    print(f"  [{i}] = 0x{val:08x}")

print()

# The key derivation at 0x1240-0x125d loop:
# for i in range(4):
#   esi = table2[i]  # r8+i*4
#   edx = table1[i]  # rdi+i*4  
#   edx ^= ebx  # hash
#   edx ^= esi
#   key[i] = edx
#
# Then if r9d != 0 (piping/not-tty):
#   key[0] ^= 0xdeadbeef

print("=== XTEA Analysis ===")
print()
print("XTEA decrypt at 0x2940:")
print("  - Takes: key (rbp=rdi), ciphertext ptr (rsi), length in blocks (rcx)")
print("  - XTEA with delta=0x9e3779b9, 32 rounds")
print()

print("=== Feed.bin Analysis ===")
with open('feed.bin', 'rb') as f:
    feed = f.read()

print(f"feed.bin size: {len(feed)} bytes = {len(feed)//8} 64-bit blocks = {len(feed)//8} XTEA block-pairs")

# The key is derived from:
# 1. A murmur-hash of some section of the binary (the text section or data section)  
# 2. XOR'd with table1 and table2 from .rodata
# 3. Optionally XOR'd with 0xdeadbeef if not a tty

# The stdin input handling (function at 0x4370):
# It reads from /dev/tty (fd=2 then open("/dev/tty")?), no...
# Actually looking at chk section 0x4370:
# - opens "/dev/tty" (edi=2 -> AF_INET??)... no
# - Actually edi=2 means O_RDWR for open, but first arg is 2...
# Wait, looking again: at 0x437b: mov edi, 2 -> this is the file descriptor! fd=2 = stderr

# Actually at 0x4370 in chk:
# sub rsp, 0x1068
# xor ecx, ecx; xor edx, edx; mov edi, 2  -> syscall args for read(2, ...)
# Then: lea rsi, [rsp+0x30]; call 0x4340 (syscall wrapper) -> read(2, buf, 0xfff)
# fd=2 = stderr... hmm but the program writes to stdout and reads from stdin?

# Actually looking more carefully at 0x4340:
# mov rax, rdi; mov rdi, rsi; mov rsi, rdx; mov rdx, rcx; syscall
# So chk_syscall(rax, rdi, rsi, rdx) = syscall(rdi, rsi, rdx, rcx) ... wait no
# It's: rax=rdi, rdi=rsi, rsi=rdx, rdx=rcx -> syscall
# So: chk_syscall(syscall_nr, arg1, arg2, arg3)

# At 0x4370:
# xor ecx, ecx; xor edx, edx; mov edi, 2 -> not args yet
# lea rsi, [rsp+0x30]
# movzx r9d, [rsp+0x1f]  -> r9d = 0x5a ('Z')
# movd xmm0, r9d; mov eax, r9d
# punpcklbw, punpcklwd, pshufd -> fill xmm0 with 0x5a5a5a5a...
# pxor xmm0, [rip+0x2c76] -> xmm0 ^= [0x43c2+0x2c76+11]... let me compute
# 0x43c2 + 7 = 0x43c9 (after pxor instruction?) + 0x2c76 = 0x703f ?
# Hmm let me recheck: at 0x43c2: pshufd xmm0, xmm0, 0 (4 bytes)
# next at 0x43c7(?): pxor xmm0, [rip+0x2c76] 
# Actually in disasm: 0x43c2: pshufd xmm0, xmm0, 0 -> 4 bytes? let me check hex:
# 0x43c2: 66 0f 70 c0 00 -> 5 bytes (pshufd r/m64, r/m64, imm8 with 66 prefix)
# so next at 0x43c7: pxor xmm0, xmmword ptr [rip+0x2c76]
# rip = 0x43c7 + 8 = 0x43cf, target = 0x43cf + 0x2c76 = 0x7045... in .rodata

# Let me look at what's at 0x7045 in rodata:
print()
print("=== .rodata contents ===")
for i in range(0, min(0x100, rodata_size), 16):
    off = rodata_off + i
    hex_part = ' '.join(f'{b:02x}' for b in data[off:off+16])
    asc_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[off:off+16])
    va = 0x7000 + i
    print(f"0x{va:04x}({off:#06x}): {hex_part}  {asc_part}")
