## Captain Mark Compass — Writeup

### Summary
The logbook outputs come from a Markov‑switching LCG. Each step updates

```
s_{t+1} = a_i * s_t + b_i (mod P)
```

and then the state (which selects the next `(a, b)` pair) is chosen by a
Markov transition matrix. We’re given 850 consecutive outputs and a ciphertext
that uses the next outputs’ low bytes as a keystream.

### 1) Recover the modulus
For a *constant* LCG, the standard determinant

```
d3*d1 - d2*d2 ≡ 0 (mod P)
```

with `d1 = s1 - s0`, `d2 = s2 - s1`, `d3 = s3 - s2`.

Because the Markov chain often stays in the same state, many *runs* of four
outputs use the same `(a, b)` and therefore yield determinants that are
multiples of `P`. Taking GCDs of many such determinants recovers the prime
modulus.

### 2) Recover the heads `(a, b)`
Any triple `(s0, s1, s2)` uniquely defines the affine map that sends
`s0 -> s1 -> s2`:

```
a = (s2 - s1) * (s1 - s0)^(-1) mod P
b = s1 - a*s0 mod P
```

True heads appear many times (whenever the chain stays in the same state for
two transitions), so counting repeats gives all heads. In this logbook there
are 5.

### 3) Recover the state sequence
With `P` and the heads, each transition `s_{t-1} -> s_t` is matched to the
unique head satisfying `s_t = a*s_{t-1} + b (mod P)`. This yields the observed
state sequence and allows estimating the transition probabilities.

### 4) Decrypt the flag
The keystream byte for each flag byte is `s_next & 0xFF`. We start from the
last logbook value and try all possible next states (5 choices). A constrained
BFS keeps only candidates that look like a flag (`prefix{...}` with sane
characters and a closing `}` at the end). That produces a small candidate set.

Finally, score each candidate’s state sequence using the empirical Markov
transition probabilities and pick the most likely path.

### Flag

```
RS{w04h_h1dd3n_M4rk0v_br34k5_LCGs}
```
