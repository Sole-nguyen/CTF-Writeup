import os

def advanced_zwc_decode(filename):
    print(f"[*] Đang phân tích ZWC từ {filename}...")
    try:
        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
    except Exception as e:
        print(f"[-] Lỗi đọc file: {e}")
        return

    zwc_list = [c for c in content if c in ['\u200b', '\u200c']]
    char_0, char_1 = '\u200b', '\u200c'
    
    bin1 = "".join(['0' if c == char_0 else '1' for c in zwc_list])
    bin2 = "".join(['1' if c == char_0 else '0' for c in zwc_list])
    
    def bin_to_bytes(b_str, little_endian=False):
        res = bytearray()
        for i in range(0, len(b_str), 8):
            byte_str = b_str[i:i+8]
            if len(byte_str) == 8:
                if little_endian:
                    byte_str = byte_str[::-1]
                res.append(int(byte_str, 2))
        return bytes(res)

    # 4 trường hợp có thể xảy ra
    variants = {
        "Map1_BigEndian": bin_to_bytes(bin1, False),
        "Map1_LittleEndian": bin_to_bytes(bin1, True),
        "Map2_BigEndian": bin_to_bytes(bin2, False),
        "Map2_LittleEndian": bin_to_bytes(bin2, True),
    }

    print(f"[*] Đã giải mã thành {len(variants['Map1_BigEndian'])} bytes. Tiến hành kết xuất...\n")

    for name, data in variants.items():
        print(f"--- {name} ---")
        safe_text = "".join([chr(b) if 32 <= b <= 126 else '.' for b in data[:100]])
        print(f"Preview: {safe_text}")
        out_name = f"zwc_{name}.bin"
        with open(out_name, 'wb') as out_f:
            out_f.write(data)

if __name__ == '__main__':
    advanced_zwc_decode('empty.js')