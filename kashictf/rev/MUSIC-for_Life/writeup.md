# MUSIC-for_Life Writeup

## Flag

`kashiCTF{MUSIC_VIBES_but_all_1_w4nt_15_a_zsRl2y}`

## Analysis

The downloaded `file.bin` is a mono 16-bit PCM WAV at 44.1kHz.

The provided `keyboard` ELF reveals the encoder logic:

1. For each input byte `c`, it computes:
   - `t = ((c ^ 0xA5) + 0x11) & 0xFF`
   - `freq = 500 + 9 * t`
2. It emits a sine wave for `0.12s` (`5292` samples) at that frequency:
   - `sample[i] = int(28000 * sin(2*pi*freq*i/44100))`

So each character is one fixed-size audio block.

## Decoding trick

For each `5292`-sample block, use sample at index `1`:

- `sample[1] = 28000 * sin(2*pi*freq/44100)`

Thus:

- `freq = asin(sample[1]/28000) * 44100 / (2*pi)`
- `t = round((freq - 500)/9) & 0xFF`
- `c = ((t - 0x11) & 0xFF) ^ 0xA5`

Applying this across all blocks recovers:

`kashiCTF{MUSIC_VIBES_but_all_1_w4nt_15_a_zsRl2y}`
