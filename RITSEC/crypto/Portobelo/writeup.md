# Portobelo — Writeup

The server exposes a `QUERY <A>` endpoint that returns:

```
RESULT j_inv ops_count trace
```

The only secret-dependent value is:

```
trace(A) = sum_{i != poisoned} secret_key[i] * A^i  (mod p)
```

So each query is a polynomial evaluation over `F_p` where one coefficient is removed. With enough distinct `A`, we can interpolate the polynomial and recover all coefficients except the poisoned slot (which becomes `0` in the interpolated result).

## Steps

1. **Collect points.** Query `n = len(primes)` distinct `A` values (avoid `A^2 = 4`) to get `trace(A)` values.
2. **Interpolate.** Solve the Vandermonde system modulo `p` to recover polynomial coefficients. Convert them to small signed integers (using centered reduction).
3. **Recover the missing exponent.** `ops_count = sum(abs(secret_key[i]))` is leaked.  
   Compute `abs_missing = ops_count - sum(abs(recovered[i]))`.  
   The poisoned index is one of the positions where the recovered coefficient is `0`. Try inserting `±abs_missing` at those positions.
4. **Derive AES key.** Use the provided KDF (`gr48_poly`, `gr48_generator`) with the reconstructed `secret_key`.
5. **Decrypt.** AES-GCM with the supplied nonce/tag verifies the correct key and yields the flag.

## Solver

`solve.py` implements the above:

- Parses `PARAMS` and `ENCRYPTED_FLAG`
- Performs `n` queries
- Interpolates coefficients via Gaussian elimination mod `p`
- Uses `ops_count` to recover the poisoned entry
- Attempts all remaining candidates and validates with AES-GCM

Run:

```
python3 solve.py
```

Flag: `RS{504_1s_7smo0th_s0_th3_0rb1t_h4s_n1n3}`

