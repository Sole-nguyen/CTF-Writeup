import struct

def decode_double(hex_le):
    b = bytes.fromhex(hex_le)
    return struct.unpack('<d', b)[0]

THRESHOLD = decode_double('95d626e80b2e113e')
CONV_EPS  = decode_double('8dedb5a0f7c6b03e')

def simulate(x, y):
    c1 = c2 = 0
    while c2 <= 49:
        rf  = x**3 - 3*x*y**2 - 1.0
        imf = 3*x**2*y - y**3
        rfp = 3*(x**2 - y**2)
        ifp = 6*x*y
        fpsq = rfp**2 + ifp**2
        if fpsq < THRESHOLD:
            break
        x -= (rf*rfp + imf*ifp) / fpsq
        y -= (imf*rfp - rf*ifp) / fpsq
        c1 += 1
        if abs(x - 1) < CONV_EPS and abs(y) < CONV_EPS:
            break
        c2 += 1
    return c1

# Load and classify all points
pixels = []
with open('signal_data.txt') as f:
    for line in f:
        x, y = map(float, line.split(','))
        pixels.append(1 if simulate(x, y) == 12 else 0)

# Render as 130x20 grid
W = 130
for row in range(20):
    line = ''.join('#' if pixels[row * W + col] else '.' for col in range(W))
    print(f"R{row:2d}: {line}")