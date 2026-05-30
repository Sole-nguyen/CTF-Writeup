import random

def solve():
    enc_flag_hex = "a9fa3c5e51d4cea498554399848ad14aa0764e15a6a2110b6613f5dc87fa70f17fafbba7eb5a2a5179"
    enc_flag_bytes = bytes.fromhex(enc_flag_hex)
    shuffled_bits = []
    for b in enc_flag_bytes:
        shuffled_bits.extend(list(bin(b)[2:].zfill(8)))
    length = len(shuffled_bits)
    text = "I_LOVE_RNG"
    m = int.from_bytes(text.encode(), "big")
    e = 7
    seed = m ** e
    indices = list(range(length))
    for i in range(10):
        random.seed(seed * (i + 1))
        random.shuffle(indices)
    original_bits = [''] * length
    for shuffled_idx, original_idx in enumerate(indices):
        original_bits[original_idx] = shuffled_bits[shuffled_idx]
    flag = ""
    for i in range(0, length, 8):
        byte_str = "".join(original_bits[i:i+8])
        flag += chr(int(byte_str, 2))
    print(f"[+] Recovered Flag: {flag}")
if __name__ == "__main__":
    solve()
