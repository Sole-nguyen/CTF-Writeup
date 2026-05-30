# Ghaat Mirage — Writeup

The binary is UPX-packed and intentionally prints a decoy flag on the obvious path.

## 1. Spot the decoy

Running `./prog anything` always prints:

`kashi{fr4ke_g4ng4_0ffering_lol}`

So this path is fake.

## 2. Unpack and inspect real logic

Unpack with a newer UPX:

```bash
upx -d -o prog_unpacked prog
```

Disassembly of `prog_unpacked` shows:

1. `main` computes FNV-1a-like hash of first up to 9 bytes.
2. It does `hash % 0xfb` and uses that as an index into a function-pointer table.
3. Most table entries call decoy functions.
4. One entry calls the real validator at `0x1300`.

## 3. Real validator behavior

Function at `0x1300`:

1. Requires input length exactly `0x20` (32).
2. Splits positions into 4 buckets by index mod 4.
3. For each byte `c` in a bucket, updates:
   `state = state * 0x83 + c`
4. Compares final 4 states against constants:
   - `0x00fd91b66d4b8b11`
   - `0x00e661491544fdb8`
   - `0x010fc69e6442ef55`
   - `0x00f680346b31a222`

This can be reversed from the end (`state_n` -> `state_{n-1}`) by trying byte candidates satisfying modulo constraints.

Each bucket has one printable solution:

- bucket0: `ki404_ei`
- bucket1: `a{tfsNr3`
- bucket2: `sG5_he_5`
- bucket3: `hh_K1vD}`

Interleaving these bucket strings (index pattern `bucket + 4*k`) gives:

`kashi{Gh4t5_0f_K4sh1_Never_Di35}`

Binary confirms this as the true accepted offering.

## 4. Flag

Binary output format:

`kashi{Gh4t5_0f_K4sh1_Never_Di35}`
