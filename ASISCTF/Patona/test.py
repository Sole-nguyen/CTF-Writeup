with open('flag.raw', 'rb') as f:
    d = f.read()
    
# Show first 200 bytes as hex
print("Hex dump (first 200 bytes):")
for i in range(0, 200, 20):
    chunk = d[i:i+20]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    print(f"{i:04d}: {hex_str}")

print(f"\nTotal size: {len(d)} bytes")

# Decode as UTF-8
txt = d.decode('utf-8', errors='replace')
print(f"Text length: {len(txt)} characters")

# Show first 100 chars with their codes
print("\nFirst 100 characters:")
for i in range(min(100, len(txt))):
    ch = txt[i]
    print(f"{ch}", end='')
print()

print("\nFirst 100 character codes:")
for i in range(min(100, len(txt))):
    ch = txt[i]
    print(f"U+{ord(ch):04X}", end=' ')
    if (i+1) % 10 == 0:
        print()
