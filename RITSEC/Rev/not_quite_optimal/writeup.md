# not_quite_optimal

The binary loads 84 (0x54) pairs of 64-bit integers from `.rodata` at 0x22a0 and prints one character per pair. The core routine computes a tetration `f(a, b) = a ^^ b` using GMP (recursive exponent towers), then returns `((f(a, b) mod 256) + 1) >> 1`. Slow output is due to frequent `nanosleep` calls.

To solve efficiently, compute the sequence modulo 256. For a fixed base `a_mod = a % 256`, the sequence `f(1) = a_mod`, `f(n+1) = a_mod ** f(n) mod 256` has at most 256 states, so it reaches a short cycle quickly. Precompute the cycle for each base and index by `b` to get `f(a, b) mod 256`, then map to the output byte.

**Flag:** `RS{4_littl3_bi7_0f_numb3r_th30ry_n3v3r_hur7_4ny0n3_19b3369a25c78095689a38f81aa3f5e3}`
