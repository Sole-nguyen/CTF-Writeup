# Bake a Pi

**Summary:** The `C` option lets you edit an ingredient by index, but it accepts `8` even though only 0–7 are valid. Index `8` writes into the `pi` global. By overwriting that double with the real π value, the `T` option passes the taste test and `execl("/bin/bash", ...)` is reached.

## Analysis

- `ingredients` is an array of 8 strings, each 0x20 bytes at `0x404080`.
- `pi` is a double at `0x404180` initialized to `0.123456789`.
- The index check is `if (idx <= 8)` so `idx = 8` is allowed.
- Writing ingredient `8` with `fgets` writes to `0x404080 + 8 * 0x20 = 0x404180`, overlapping `pi`.
- The taste test compares `pi` to the constant `3.141592653589793` and spawns `/bin/bash` on success.

## Exploit

1. Send `C` (change ingredient).
2. Send index `8`.
3. Send the 8 raw bytes of the double `3.141592653589793` (little-endian: `18 2d 44 54 fb 21 09 40`), followed by a newline.
4. Send `T` to trigger the taste test and drop into a shell.
5. Read the flag from `./flag.txt`.

## Run

```bash
python3 solve.py
```

## Flag

`RS{0ff_by_0n3_4s_e4sy_4s_4_sk1llb17_p1}`
