# Efficient writeup

The RSA modulus generation is flawed: instead of `n = p * q`, this instance has:

`n = p^2`

That means factoring is trivial:

`p = sqrt(n)`

Then:

`phi(n) = p * (p - 1)`

so we can compute:

`d = e^{-1} mod phi(n)`

Use `d` to decrypt RSA ciphertext `ct`, which recovers the AES key (16 bytes).
Decrypt `flag_ct` with AES-CBC using provided `iv`.

Recovered flag:

`kashiCTF{wh3n_0n3_pr1m3_1s_n0t_3n0ugh_p_squared_1s_w0rs3}`

## Solver

Run:

```bash
python3 solve.py
```

Requires `pycryptodome` (`Crypto` module).
