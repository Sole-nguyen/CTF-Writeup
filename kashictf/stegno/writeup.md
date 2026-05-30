# I like to save my files as pdfs (Kashi kings hate 184) — Writeup

## Flag

`KashiCTF{ILOVEkashi}`

## Solve idea

The attachment is not a PDF. It is a malformed **P6 PPM** image:

- header says `284 x 150`
- pixel body actually contains `185` rows

So there are `35` appended hidden rows (`150..184`).  
In that appended strip, a boxed text component exists and contains the flag text.

## Why the hint mentions 184

`184` is the last row index of the hidden appended strip (`150..184`), i.e. the hidden payload zone.

## Deterministic extraction

1. Parse P6 header and pixel body.
2. Compute actual rows from body length.
3. Split hidden strip `extra = img[header_height:]`.
4. Find the largest text-like connected component in the strip.
5. Crop it, save an 8x upscaled preview image.
6. Verify crop hash for the official file and print the known flag.

For the official challenge file used here, the extracted crop SHA-256 is:

`a888b6f930b1e05a220b1e2823ac04a8d6feee389a51554fa5f279e8647ed0b0`

## Run

```bash
python3 solve.py flag.ppm
```

Example output:

```text
[+] Parsed dimensions: header=284x150, actual_rows=185
[+] Hidden strip rows: 35
[+] Located box: x=126, y=15, w=84, h=20
[+] Crop sha256: a888b6f930b1e05a220b1e2823ac04a8d6feee389a51554fa5f279e8647ed0b0
[+] Flag: KashiCTF{ILOVEkashi}
```
