import base64
import base62 # pip install pybase62
import base45 # pip install base45

cipher_base62 = "oHBnFiWdx4lOO221MKPSPfnwHdC9kV3NMnbosDDYQqw5NGhwfTMUXISW3HZyFv32aGvZGmkrM8bemfVh3dVmmKwxeFgtk1AfGyH7zbdEzmgJSntQpOhRptupMI5Ph0pkipcKO3KsidJUa9tN6RgQ7axnDKX8EzpgZhf0x8Asqko2BgUvqN74th8fUiUnM5bRTjQ1r2q3cDECPYciWEoHHWcHVLNVYqJhth0QdYYcILPbjJYZo2K9VcoEemz1AyGMaO6peEukNiVEki5uc5A9cARxvT5XQCF05v"

try:
    print("[*] Bắt đầu bóc củ hành...")
    
    # Lớp 1: Base62 -> Base45
    layer2_bytes = base62.decodebytes(cipher_base62)
    layer2_str = layer2_bytes.decode('utf-8')
    print(f"[+] Lớp 1 (Base62) OK! Dấu hiệu Base45: {layer2_str[:30]}...")

    # Lớp 2: Base45 -> Base32
    layer3_bytes = base45.b45decode(layer2_str)
    layer3_str = layer3_bytes.decode('utf-8')
    print(f"[+] Lớp 2 (Base45) OK! Dấu hiệu Base32: {layer3_str[:30]}...")

    # Lớp 3: Base32 -> Base64
    layer4_bytes = base64.b32decode(layer3_str)
    layer4_str = layer4_bytes.decode('utf-8')
    print(f"[+] Lớp 3 (Base32) OK! Dấu hiệu Base64: {layer4_str[:30]}...")

    # Lớp 4: Base64 -> Output Cuối
    flag_bytes = base64.b64decode(layer4_str)
    
    try:
        flag = flag_bytes.decode('utf-8')
        print(f"\n[+] TÌM THẤY FLAG: {flag}")
    except:
        # Đề phòng trường hợp lõi là mã Hex hoặc bytes
        print(f"\n[+] Lớp cuối cùng là raw bytes: {flag_bytes}")

except Exception as e:
    print(f"\n[-] Lỗi giải mã: {e}")