# Pierre's Compass - RITSEC CTF Crypto Challenge Writeup

## Challenge Description

Pierre, a French pirate, built an enchanted compass. Each turn of its needle is driven by three hidden mechanisms (Linear Congruential Generators) working together. We need to decode Pierre's secret message that was lost to the seas.

## Given Information

From `params.txt`, we have:
- **Alphabet**: A custom 94-character set used for encoding
- **Three LCG moduli**: m1=95, m2=37, m3=19
- **Three seeds**: s1=11, s2=29, s3=7

## What We Need to Find

Linear Congruential Generators follow the formula: `X_{n+1} = (a * X_n + c) mod m`

We need to find:
- **Multipliers (a)**: a1, a2, a3
- **Increments (c)**: c1, c2, c3

## Solution Approach

### Step 1: Understanding the System

Three LCGs work in parallel, each generating a sequence of numbers. These numbers are combined to index into the alphabet to produce the message.

### Step 2: Brute Force Search

Since the moduli are relatively small, we can brute force the parameters:
- For LCG to have a full period, `a` must be coprime to `m` (gcd(a,m) = 1)
- `c` can be any value from 0 to m-1
- The flag format RS{...} helps us identify when we've found the right parameters

### Step 3: Combining the Outputs

The three LCG outputs are combined using: `index = (state1 + state2 + state3) % alphabet_length`

This index is then used to look up the character in the alphabet.

### Step 4: Finding the Parameters

Through brute force search, we discovered:
- **Generator 1**: a1=1, c1=1
- **Generator 2**: a2=3, c2=9
- **Generator 3**: a3=10, c3=7

### Step 5: Decoding the Message

With these parameters, we decode the message by:
1. Starting with the initial seeds
2. Stepping each LCG forward
3. Combining the outputs to get an index
4. Looking up the character at that index in the alphabet
5. Repeating until we have the full message

## Important Discovery

The flag is unusually long - **238 characters**! The closing brace `}` appears at position 300 in the decoded stream, while `RS{` appears at position 63. This means we need to generate at least 301 characters to see the complete flag.

## The Flag

```
RS{\xLSP;N-M7V,GK'N*fV`r@?,/+.T">FLa/H@h$&H,3Dk:|lW5`oDzH4mYz3u[<Jpj!a$R[0zdM-0u{1tscnfomN1K0FT.K{SUq)E6@RM8UxK5|:xf@;=\Ze9y.D;`LOJ<`@H#VBwig/:[#$`Xst$Hz^hb>CIDJ1^m$_)qmz0(4vW7A[sU(MmyZ\M0KQdG!2L1)+QTM/wBTKx=F%%|rP\#S:.~bh:L`*65'p&;B^*J:}
```

## Technical Details

### LCG Parameters Validation

The parameters we found satisfy the requirements for good LCGs:
- gcd(1, 95) = 1 ✓
- gcd(3, 37) = 1 ✓
- gcd(10, 19) = 1 ✓

### Character Set

The alphabet contains special characters including backslashes and quotes, which makes the flag appear to have escape sequences like `\x`, but these are actually literal characters from the custom alphabet.

## Running the Solution

```bash
python3 solve.py
```

The script will:
1. Set up the three LCGs with the discovered parameters
2. Generate 500 characters (to ensure we capture the full flag)
3. Find and extract the complete flag between `RS{` and `}`

## Key Takeaways

1. **Small moduli make brute force feasible**: With moduli under 100, we can test all valid parameter combinations
2. **Flag format helps verification**: Looking for `RS{` in the output quickly confirms correct parameters
3. **Don't assume flag length**: This flag is much longer than typical CTF flags
4. **Custom alphabets require careful handling**: The backslashes and special characters in the alphabet need proper escaping in code

## Tools Used

- Python 3
- Basic number theory (GCD for coprimality check)
- Brute force search with early termination

## Difficulty

Medium - Requires understanding of LCGs and patience to let the brute force search run, plus careful handling of the unusually long flag.
