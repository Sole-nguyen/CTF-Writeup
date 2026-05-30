#!/usr/bin/env python3
import math
import struct
import wave


SEGMENT_SAMPLES = 0x14AC  # 5292 samples = 0.12s at 44.1kHz
SAMPLE_RATE = 44100
AMPLITUDE = 28000.0
BASE_FREQ = 500.0
STEP_FREQ = 9.0


def decode_wav(path: str) -> str:
    with wave.open(path, "rb") as w:
        if w.getnchannels() != 1 or w.getsampwidth() != 2 or w.getframerate() != SAMPLE_RATE:
            raise ValueError("Unexpected WAV format")
        frames = w.readframes(w.getnframes())

    samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)
    if len(samples) % SEGMENT_SAMPLES != 0:
        raise ValueError("Audio length is not aligned to segment size")

    out = bytearray()
    for i in range(0, len(samples), SEGMENT_SAMPLES):
        s = samples[i + 1]  # index 1 maps directly to sin(w)
        x = max(-1.0, min(1.0, s / AMPLITUDE))
        freq = math.asin(x) * SAMPLE_RATE / (2.0 * math.pi)
        transformed = round((freq - BASE_FREQ) / STEP_FREQ) & 0xFF
        ch = ((transformed - 0x11) & 0xFF) ^ 0xA5
        out.append(ch)

    return out.decode("latin1")


if __name__ == "__main__":
    print(decode_wav("file.bin"))
