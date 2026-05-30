# -*- coding: utf-8 -*-
data = [
    0x65, 0xB6, 0x89, 0x60, 0xC2, 0x33, 0x04, 0xFB, 0xCB, 0x37, 
    0xD1, 0xBC, 0x51, 0x1C, 0x89, 0x7B, 0xB2, 0x6D, 0x34, 0xAE, 
    0xAE, 0xB4, 0x8F, 0x23, 0x1F, 0x33, 0x0C, 0x5C, 0x12, 0xAB, 
    0x51, 0x51, 0x6D, 0x08, 0xC9, 0xD0, 0x6D, 0xE2, 0xF0, 0xFC, 
    0x72, 0x40
]

# The challenge mentions "Go Go Squid!"
# Maybe ROT or something with character codes?

# Try all variations of the squid message
messages = [
    "Go Go Squid!",
    "GoGoSquid!",
    "gogosquid",
    "GOGOSQUID",
    "squid",
    "SQUID",
    "Squid",
    "Symbol",
    "symbol",
    "hope",
    "Hope",
    "symbolofhope",
]

def xor_with_key(data, key):
    result = []
    key_bytes = key.encode() if isinstance(key, str) else key
    for i, b in enumerate(data):
        result.append(b ^ key_bytes[i % len(key_bytes)])
    return bytes(result)

print("=== Trying all key variations ===")
for msg in messages:
    result = xor_with_key(data, msg)
    try:
        text = result.decode('ascii')
        print(f"{msg:20s} -> {repr(text)}")
        if 'uoftctf' in text.lower() or text.isprintable():
            print(f"  *** INTERESTING: {text}")
    except:
        pass

# Maybe the title is literally the key?
# "Like a beacon in the dark, Go Go Squid! stands as a symbol of hope to those who seek to be healed."

full_message = "Like a beacon in the dark, Go Go Squid! stands as a symbol of hope to those who seek to be healed."
result = xor_with_key(data, full_message)
try:
    text = result.decode('ascii')
    if 'uoftctf' in text.lower():
        print(f"\n*** FULL MESSAGE KEY WORKS ***\n{text}")
except:
    pass

# Try just the first part
for phrase in ["beacon", "dark", "stands", "healed"]:
    result = xor_with_key(data, phrase)
    try:
        text = result.decode('ascii')
        if 'uoftctf' in text.lower() or text.isprintable():
            print(f"{phrase:20s} -> {text}")
    except:
        pass
