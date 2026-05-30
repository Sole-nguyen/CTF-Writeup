#!/usr/bin/env python3
import re
import struct
import wave
from functools import lru_cache
from pathlib import Path


WAV_PATH = Path("ade823c7-b42f-4568-85b7-4b726408e4e5.wav")


def extract_left_channel_dtmf_ascii_digits(path: Path) -> str:
    import numpy as np

    with wave.open(str(path), "rb") as w:
        fs = w.getframerate()
        ch = w.getnchannels()
        raw = w.readframes(w.getnframes())

    arr = np.frombuffer(raw, dtype="<i2").astype(np.float32)
    left = arr[0::2] if ch == 2 else arr
    sig = left / (np.max(np.abs(left)) + 1e-9)

    low = [697, 770, 852, 941]
    high = [1209, 1336, 1477, 1633]
    keys = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]

    win = int(0.05 * fs)
    hop = int(0.01 * fs)
    vals = []

    for st in range(0, len(sig) - win, hop):
        x = sig[st : st + win] * np.hanning(win)
        n = np.arange(win)
        lp = []
        hp = []
        for f in low:
            c = np.exp(-2j * np.pi * f * n / fs)
            lp.append(abs((x * c).sum()))
        for f in high:
            c = np.exp(-2j * np.pi * f * n / fs)
            hp.append(abs((x * c).sum()))

        lp = np.array(lp)
        hp = np.array(hp)
        li = int(lp.argmax())
        hi = int(hp.argmax())
        lmax, hmax = lp[li], hp[hi]
        l2, h2 = np.partition(lp, -2)[-2], np.partition(hp, -2)[-2]
        if lmax > 1.8 * l2 and hmax > 1.8 * h2 and lmax > 5 and hmax > 5:
            vals.append((st / fs, keys[li][hi]))
        else:
            vals.append((st / fs, None))

    seq = []
    cur = None
    start = None
    cnt = 0
    for t, k in vals:
        if k == cur:
            cnt += 1
        else:
            if cur is not None and cnt >= 3:
                seq.append((start, t, cur, cnt))
            cur, start, cnt = k, t, 1
    if cur is not None and cnt >= 3:
        seq.append((start, vals[-1][0], cur, cnt))

    digits = "".join(x[2] for x in seq if x[2].isdigit())
    return digits


def decode_ascii_stream_from_digits(digits: str) -> str:
    @lru_cache(None)
    def best(i):
        if i == len(digits):
            return ("", 0)
        best_s = None
        best_sc = -10**9
        for ln in (2, 3):
            if i + ln > len(digits):
                continue
            n = int(digits[i : i + ln])
            if 32 <= n <= 126:
                ch = chr(n)
                tail, sc = best(i + ln)
                if tail is None:
                    continue
                bonus = 2
                if ch.isalnum() or ch in "_{}":
                    bonus += 2
                if ch in "{}":
                    bonus += 5
                cand = ch + tail
                csc = sc + bonus
                if csc > best_sc:
                    best_s, best_sc = cand, csc
        return (best_s, best_sc)

    out, _ = best(0)
    return out or ""


def main():
    digits = extract_left_channel_dtmf_ascii_digits(WAV_PATH)
    decoded = decode_ascii_stream_from_digits(digits)
    print("[+] Raw digit stream:")
    print(digits)
    print("\n[+] Decoded text:")
    print(decoded)
    m = re.search(r"(?:cyh|jctf|spartanCTF)\{[^}]+\}", decoded, re.I)
    if m:
        print("\n[+] Flag-like string:")
        print(m.group(0))


if __name__ == "__main__":
    main()

