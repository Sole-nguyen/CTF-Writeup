from aes import AES
key = bytes.fromhex("26ab77cadcca0ed41b03c8f2e5cdec0c")
enc_flag = bytes.fromhex("8e70387dc377a09cbc721debe27c468157b027e3e63fe02560506f70b3c72ca19130ae59c6eef47b734bb0147424ec936fc91dc658d15dee0b69a2dc24a78c44")
cipher = AES(key)
print(b"".join([cipher.decrypt(enc_flag[i:i+16]) for i in range(0, len(enc_flag), 16)]))