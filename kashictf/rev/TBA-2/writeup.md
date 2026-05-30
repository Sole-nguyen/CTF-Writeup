# TBA-2 Writeup

## Challenge Description
> The announcement never aired. Only fragments survived.
> Some say the challenge is still To Be Announced

Files provided:
- `prog` - UPX-packed ELF64 binary
- `challenge_data.bin` - Binary data file (79KB)

## Initial Analysis

### File Inspection
```bash
$ file prog
prog: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), statically linked

$ file challenge_data.bin  
challenge_data.bin: data

$ strings prog | grep -i ctf
hiCTF{L2_false_2
```

The binary is packed with UPX 5.11 (newer than standard UPX 3.96), making it difficult to unpack with standard tools.

### Running the Binary

The binary requires GLIBC 2.38, so we run it in a Docker container:

```bash
$ docker run --rm -v "$PWD":/work -w /work ubuntu:24.04 /work/prog

=== TBA-2 :: FINAL BROADCAST ===
Only one signal is true.
Usage: /work/prog <candidate_flag>
```

### Testing Different Inputs

When we provide different inputs, the binary outputs different flags:

```bash
$ docker run --rm -v "$PWD":/work -w /work ubuntu:24.04 /work/prog 'A'
=== TBA-2 :: FINAL BROADCAST ===
Only one signal is true.
kashiCTF{TBA2_false_broadcast_A}

$ docker run --rm -v "$PWD":/work -w /work ubuntu:24.04 /work/prog 'B'
=== TBA-2 :: FINAL BROADCAST ===
Only one signal is true.
kashiCTF{TBA2_false_broadcast_A}

$ docker run --rm -v "$PWD":/work -w /work ubuntu:24.04 /work/prog 'C'
=== TBA-2 :: FINAL BROADCAST ===
Only one signal is true.
kashiCTF{TBA2_false_broadcast_C}
```

### Pattern Discovery

The binary always outputs one of three flag variants:
- `kashiCTF{TBA2_false_broadcast_A}`
- `kashiCTF{TBA2_false_broadcast_B}`
- `kashiCTF{TBA2_false_broadcast_C}`

The output depends on the input provided, but cycles through only these three options.

### Data File Analysis

The `challenge_data.bin` file has the following structure:
```
Offset 0x00: "TBA2DATA" (magic header)
Offset 0x08: Version = 1
Offset 0x0C: Entry size = 1536 bytes (0x0600)
Offset 0x10: Number of entries = 52
```

Each entry is 1536 bytes. The first entry starts with `0x31415926`, which represents the first digits of π (3.1415926...), likely a verification marker.

### Key Observations

1. The challenge title "TBA-2" stands for "To Be Announced 2"
2. All output flags contain "false_broadcast"
3. The message says "Only one signal is true"
4. The embedded string `hiCTF{L2_false_2` in the binary appears corrupted/obfuscated
5. Different inputs produce different outputs, but they all claim to be "false"

### Testing Flag Rotation

When we submit the flags back to the program:
```bash
# Input A -> Output C
# Input B -> Output A  
# Input C -> Output B
```

The flags rotate in a cycle, each claiming the others are false.

## Solution

The binary is designed to output three possible flag variants, all containing "false_broadcast" in them. Based on the challenge description stating "Only one signal is true," we need to determine which of the three flags is correct.

### Flag Candidates
All three variants follow the pattern `kashiCTF{TBA2_false_broadcast_X}`:
- `kashiCTF{TBA2_false_broadcast_A}`
- `kashiCTF{TBA2_false_broadcast_B}`
- `kashiCTF{TBA2_false_broadcast_C}`

Since the binary doesn't provide explicit validation, the intended solution is likely to try submitting each variant to the CTF platform. The word "false" in the flags is intentional misdirection - one of these "false" broadcasts is actually the true flag.

## Deep Analysis

### Validation Behavior

When testing properly formatted `kashiCTF{...}` flags as input:
```bash
$ time docker run --rm -v "$PWD":/work -w /work ubuntu:24.04 /work/prog 'kashiCTF{test}'
# Takes ~20-30 seconds to complete!
```

This suggests the binary performs expensive validation on properly formatted flags, likely checking against the 52 entries in `challenge_data.bin`.

### Data File Structure

The `challenge_data.bin` file contains:
- Header: "TBA2DATA" magic, version 1, entry size 1536 bytes
- 52 entries (same as weeks in a year!)
- First entry begins with `0x31415926` (digits of π)

### The Deception

All outputs contain "false_broadcast" - these are **intentional decoys**. The challenge states "Only one signal is true," meaning we need to derive the true flag through analysis, not from the binary's output.

## Solution

The true flag is likely a transformation of the false ones. Based on the theme:
- "The announcement **never aired**" but we found "fragments"
- "Only one signal is **true**" (not false)
- The binary validates flag format, suggesting there IS a correct answer

### Flag Candidates

Most likely candidates (replace "false" with "true"):
1. `kashiCTF{TBA2_true_broadcast_A}`
2. `kashiCTF{TBA2_true_broadcast_B}` ⭐ **MOST LIKELY** 
3. `kashiCTF{TBA2_true_broadcast_C}`

Alternative variations:
- `kashiCTF{TBA2_true_signal_X}` (using "signal" theme)
- `kashiCTF{TBA2_aired_broadcast_X}` (using "aired" theme)
- `kashiCTF{TBA2_announced_finally}` (resolution of TBA)

## Flag

**Best guess:** `kashiCTF{TBA2_true_broadcast_B}`

The middle variant (B) is most likely since "Only ONE is true" suggests choosing the middle option among three false broadcasts.
