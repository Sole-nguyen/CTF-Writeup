from PIL import Image
from pypdf import PdfReader
from pypdf.filters import decode_stream_data
import os

r = PdfReader('Untitled_document.pdf')
page = r.pages[0]
xobj = page['/Resources']['/XObject'].get_object()

os.makedirs('rendered', exist_ok=True)
for name, ref in xobj.items():
    obj = ref.get_object()
    if obj.get('/Subtype') != '/Image':
        continue

    w, h = int(obj['/Width']), int(obj['/Height'])
    rgb = decode_stream_data(obj)
    img = Image.frombytes('RGB', (w, h), rgb)

    sm = obj.get('/SMask')
    if sm:
        sm = sm.get_object()
        a = decode_stream_data(sm)
        alpha = Image.frombytes('L', (int(sm['/Width']), int(sm['/Height'])), a)
        if alpha.size != img.size:
            alpha = alpha.resize(img.size)
        img = img.convert('RGBA')
        img.putalpha(alpha)
    else:
        img = img.convert('RGBA')

    img.save(f'rendered/{name[1:]}.png')