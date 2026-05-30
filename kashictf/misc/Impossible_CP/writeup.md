# Impossible Challenge — Writeup

The challenge is **not** impossible.  
The checker has an off-by-one style validation bug: it allows queries with `i = n`, even though the statement says only `1 <= i <= n-1` is allowed.

## Key observation

Query format:

`? i x`

Response is:

- `0` if `A[i] & x == 0`
- `1` otherwise

If we can query `i = n`, we can recover `A[n]` directly, bit by bit.

For each bit `b` from `0..31`:

1. Send `? n (1<<b)`.
2. If response is `1`, then bit `b` of `A[n]` is set.
3. Reconstruct full `A[n]`, then send `! A[n]`.

This uses exactly **32 queries per testcase**, far below the limit (`20n`).

## Why this works

From local checker behavior:

- Sending `? n x` is accepted and returns a valid bit-answer.
- So the hidden last element is directly queryable, contradicting intended rules.

## Exploit script

`solve.py` implements this:

- Reads `t`, and for each testcase reads `n`
- Queries `? n 1<<b` for all 32 bits
- Sends `! recovered_value`
- Parses trailing output for `kashiCTF{...}`

## Usage

Remote:

```bash
python3 solve.py --host 34.126.223.46 --port 17738