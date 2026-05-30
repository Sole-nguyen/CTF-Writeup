# Do you even know what ret is?

Flag: `kashiCTF{made_u_return_lol_G8va7hwnYg}}`

The binary reads:
1. `n` = number of writes
2. Repeats `n` times: read `index`, then read `value` into `arr[index]`

In `main`, `arr` is a stack array of 10 integers (`arr[10]`) at `rbp-0x30`.
There is no bounds check on `index`, so this is an arbitrary stack write primitive (4-byte granularity).

The saved return address is at `rbp+0x8`.
Distance from `arr` base (`rbp-0x30`) to return address:

`0x38` bytes = `14 * 4` bytes

So writing to `arr[14]` overwrites the low 4 bytes of RIP.

Because the binary is non-PIE, `print_flag` has a fixed address:

`print_flag = 0x4011c9` (decimal `4198857`)

`main` returns with high 32 bits already zero in canonical userspace addresses here, so overwriting only the low 32 bits is enough to redirect execution.

## Exploit input

We do two writes:
1. harmless write to `arr[15]` with `0`
2. overwrite saved RIP at `arr[14]` with `4198857`

Payload:

```text
2
15
0
14
4198857
```

When `main` returns, execution jumps to `print_flag()` and prints `flag.txt`.

## Solver

Use:

```bash
python3 solve.py
```

Or custom host/port:

```bash
python3 solve.py <host> <port>
```
