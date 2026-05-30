def decompress_feshar(input_file):
    try:
        with open(input_file, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    output = bytearray()
    
    # Dữ liệu được ghi theo từng cặp 2 byte
    # Byte 1: Token ((Distance << 3) | Length)
    # Byte 2: Literal (Ký tự tiếp theo)
    
    i = 0
    while i < len(data):
        if i + 1 >= len(data):
            break # Tránh lỗi nếu file lẻ byte (không nên xảy ra)

        token = data[i]
        literal = data[i+1]
        
        # Tách Length (3 bit thấp) và Distance (5 bit cao)
        length = token & 0x07
        distance = token >> 3
        
        # Nếu có chuỗi lặp (Length > 0), copy từ quá khứ
        if length > 0:
            if distance > len(output):
                print("Error: Distance lớn hơn độ dài dữ liệu hiện tại.")
                # Trong trường hợp này logic LZ77 bị lỗi hoặc file hỏng
            else:
                start_pos = len(output) - distance
                # Copy 'length' byte từ quá khứ
                for j in range(length):
                    output.append(output[start_pos + j])
        
        # Luôn luôn thêm ký tự Literal
        output.append(literal)
        
        # Chuyển sang cặp byte tiếp theo
        i += 2

    return output

# Chạy giải mã
decoded_data = decompress_feshar("flag.fshr")

if decoded_data:
    print("--- Decoded Flag ---")
    try:
        print(decoded_data.decode("utf-8"))
    except UnicodeDecodeError:
        print(decoded_data)
        print("(Output contains binary data)")
    
    # Ghi ra file để chắc chắn
    with open("flag_decoded", "wb") as f:
        f.write(decoded_data)
    print("\nSaved decoded content to 'flag_decoded'")