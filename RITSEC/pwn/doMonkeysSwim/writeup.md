# doMonkeysSwim - Writeup

**Flag:** `RS{wh3r3_h4s_4ll_th3_rum_g0n3_mr_m0nk3y_m4n?}`

## Summary
The binary is a 64-bit static ELF with NX and stack canaries enabled, no PIE. Two bugs make exploitation possible:

1. **OOB stack leak** in `monkey_see` (reads `qword [rbp + idx*8 - 0x20]` with no bounds check).
2. **Stack overflow** in `monkey_do` (`fgets` size 0x28 into a 0x18 buffer), allowing a canary-preserving overwrite of the **saved RBP**.

We leak the canary, place a ROP chain in the global `bed` buffer via `monkey_swaperoo`, then partially overwrite the saved RBP to pivot the stack into `bed` when the game exits.

## Key Offsets and Gadgets

- `bed` global: `0x4cca60`
- `pop rdi; ret`: `0x401f43`
- `pop rsi; ret`: `0x401f45`
- `pop rdx; ret`: `0x401f47`
- `pop rax; ret`: `0x401f49`
- `syscall`: `0x401349`

## Exploit Strategy

1. **Leak canary** using `monkey_see` with index `3`.
2. **Write ROP chain into `bed`** using `monkey_swaperoo`. The first 8 bytes of `bed` are set to the canary so the corrupted `rbp` in `game` still passes its canary check.
3. **Overflow `monkey_do`** with:
   - `0x18` padding
   - leaked canary (8 bytes)
   - **7-byte overwrite** of saved RBP to `bed + 8` (fits within `fgets` max 39 bytes)
4. **Exit game** (option `6`) to trigger `leave; ret` in `game`, pivoting into `bed` and executing the ROP chain.

The ROP chain sets registers for `execve("/bin/sh", 0, 0)` and triggers `syscall`.

## Run

Local:
```bash
python3 solve.py
```

Remote:
```bash
python3 solve.py REMOTE=1
```
