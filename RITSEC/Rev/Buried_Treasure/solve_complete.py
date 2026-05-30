#!/usr/bin/env python3

def rc4_decrypt(data, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    res = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        res.append(byte ^ S[(S[i] + S[j]) % 256])
    return res

with open('buried_treasure', 'rb') as f:
    layer1_data = f.read()

key1_offset = 0x240
data1_offset = 0x465
size1 = len(layer1_data) - data1_offset

key1 = layer1_data[key1_offset:key1_offset + 16]
encrypted1 = layer1_data[data1_offset:data1_offset + size1]

layer2_data = bytearray()
for i in range(len(encrypted1)):
    layer2_data.append(encrypted1[i] ^ key1[i % 16])

with open('layer2_binary', 'wb') as f:
    f.write(layer2_data)

key2_offset = 0x240
data2_offset = 0x465
size2 = len(layer2_data) - data2_offset

key2 = layer2_data[key2_offset:key2_offset + 16]
encrypted2 = layer2_data[data2_offset:data2_offset + size2]

layer3_data = bytearray()
for i in range(len(encrypted2)):
    layer3_data.append(encrypted2[i] ^ key2[i % 16])

with open('layer3_binary', 'wb') as f:
    f.write(layer3_data)

key3 = layer3_data[0x240:0x240 + 16]
data3_offset = 0x485
size3 = 0x512F8
encrypted3 = layer3_data[data3_offset:data3_offset + size3]

final_binary = rc4_decrypt(encrypted3, key3)

with open('final_binary', 'wb') as f:
    f.write(final_binary)

print("[+] Extraction complete!")
print("[+] Final binary saved to: final_binary")

if b'RITSEC{' in final_binary:
    start = final_binary.find(b'RITSEC{')
    end = final_binary.find(b'}', start)
    if end > start:
        flag = final_binary[start:end+1].decode()
        print(f"[!] FLAG FOUND: {flag}")
else:
    print("[*] No flag found in final binary. Try running it:")
    print("    chmod +x final_binary && ./final_binary")
