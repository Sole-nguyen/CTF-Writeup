# Deep Down — Writeup

**Category:** Misc  
**Artifact:** `CHALL.gif`

## Summary
The GIF hides data in the palette index bit plane. Extracting bit 1 (the second least-significant bit) of each pixel’s palette index reveals the flag.

## Steps
1. Unzip and inspect the GIF to confirm it is palette‑indexed and has multiple frames.
2. Extract the second least‑significant bit from the palette index for each pixel per frame.
3. View the first bit‑plane frame; the flag appears as readable text.

```python
from PIL import Image
from pathlib import Path

gif_path = 'CHALL.gif'
out_dir = Path('/tmp/deepdown/pal')
out_dir.mkdir(parents=True, exist_ok=True)

im = Image.open(gif_path)
idx = 0
try:
    while True:
        im.seek(idx)
        frame = im.convert('P')
        w, h = frame.size
        data = list(frame.getdata())
        bit1 = Image.new('L', (w, h))
        bit1.putdata([255 if ((p >> 1) & 1) else 0 for p in data])
        bit1.save(out_dir / f'bit1_{idx:02d}.png')
        idx += 1
except EOFError:
    pass
PY
```

Picture: 

## Flag
```
UMASS{1N_A_G1774}
```
