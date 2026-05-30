from PIL import Image
from pathlib import Path

gif_path = 'CHALL.gif'
out_dir = Path('\output')
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