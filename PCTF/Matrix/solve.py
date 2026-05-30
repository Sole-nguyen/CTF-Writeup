def main():
    # Read ciphertext as raw bytes
    with open("cipher.txt", "rb") as f:
        ct = f.read()

    # Read leaked states (one integer per line)
    states = []
    with open("keystream_leak.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            states.append(int(line))

    # Build keystream bytes from the lowest byte of each state
    keystream = bytes([s & 0xFF for s in states])

    if len(keystream) < len(ct):
        raise ValueError(
            f"Not enough keystream bytes: have {len(keystream)}, need {len(ct)}"
        )

    # XOR ciphertext with keystream
    pt = bytes([c ^ keystream[i] for i, c in enumerate(ct)])

    try:
        print("Plaintext:", pt.decode("utf-8"))
    except UnicodeDecodeError:
        # Fallback if it is not valid UTF-8
        print("Plaintext (bytes):", pt)
    print("Flag likely:", pt.decode("utf-8", errors="ignore"))

if __name__ == "__main__":
    main()