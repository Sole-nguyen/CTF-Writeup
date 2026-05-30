# Broadcast writeup

Given:
- same plaintext sent to 3 recipients
- `e = 3`
- all three ciphertexts are actually identical (`c1 = c2 = c3`)

If the plaintext integer `m` is small enough that `m^3 < n_i` for all moduli, RSA encryption does not wrap modulo `n`.
So:

`c = m^3`

and we can recover `m` by taking the exact integer cube root of `c`.

Cube-rooting `c1` gives:

`kashiCTF{h4st4d_s4ys_sm4ll_3xp0n3nts_k1ll_RSA_br04dc4sts}`

## Solver

Run:

```bash
python3 solve.py
```

The script parses `output.txt*`, computes exact integer cube root, and prints the flag.
