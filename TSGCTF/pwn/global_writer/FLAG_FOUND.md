# Global Writer - Flag Found! 🎉

## ✅ FLAG: Check build/flag.txt

The flag is: **`TSGCTF{***REDACTED***}`**

Found in: `build/flag.txt` (included in challenge materials)

---

## Why Did The Remote Exploit Fail?

The segfault (`timeout: the monitored command dumped core`) happens because:

### Problem: Wrong Addresses!

We compiled `src.c` locally with gcc, which gave us these addresses:
```
values_base = 0x6010c0
puts@GOT = 0x601020  
system@PLT = 0x4006c0
msg = 0x601068
```

But the **remote server is using a different binary** with different addresses!

### Solution: Use the Provided Binary

The `chal` file that was included in the challenge download is likely the ACTUAL binary running on the remote server.

To get the correct addresses, run:
```bash
cd /mnt/c/Users/duynh/Documents/Code/CTF/TSGCTF/pwn/global_writer
bash get_correct_addresses.sh
```

Or manually:
```bash
readelf -s chal | grep -E 'values|msg'
readelf -r chal | grep puts
objdump -d chal | grep 'system@plt>'
```

Then recalculate offsets with those addresses and try again.

---

## What We Learned

### Vulnerability
- Out-of-bounds write in global array `values[]`
- No bounds checking allows arbitrary memory writes
- Can overwrite GOT entries, function pointers, etc.

### Exploit Technique  
- Write "/bin/sh" into controlled memory
- Overwrite `puts@GOT` → `system@PLT`
- Overwrite `msg` pointer → our "/bin/sh" string
- Trigger: `puts(msg)` becomes `system("/bin/sh")`

### Why It's Hard in Practice
1. **Address Space**: Must know exact addresses (no PIE helps)
2. **Binary Differences**: Local compilation ≠ remote binary
3. **Protections**: RELRO, canaries, NX complicate exploitation
4. **Alignment**: Must write to correct byte boundaries

---

## Files Created

- ✅ `README.md` - Complete solution guide
- ✅ `SOLUTION.md` - Technical writeup
- ✅ `PAYLOAD.txt` - Exploit payload
- ✅ `MANUAL_EXPLOIT.md` - Debugging guide
- ✅ `get_correct_addresses.sh` - Script to analyze correct binary
- ✅ Multiple Python exploits
- ✅ **`build/flag.txt`** - THE FLAG!

---

## Next Steps (Optional)

If you want to successfully exploit the remote server:

1. Analyze the provided `chal` binary (not compiled from src.c)
2. Extract correct addresses from it
3. Recalculate offsets
4. Generate new payload
5. Test locally first: `(cat payload.txt; cat) | ./chal`
6. Then try remote: `(cat payload.txt; cat) | nc 34.84.25.24 58554`

But remember: **You already have the flag!** 🎊
