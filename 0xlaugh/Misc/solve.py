def solve_arch(file_content):
    # Khởi tạo bộ nhớ (tape) và con trỏ (pointer)
    tape = [0] * 30000
    ptr = 0
    
    # Ánh xạ các từ khóa sang lệnh Brainfuck
    # Tách chuỗi dựa trên khoảng trắng và xuống dòng
    tokens = file_content.split()
    
    # Logic ánh xạ chuẩn của ngôn ngữ "I use Arch btw"
    bf_mapping = {
        "arch": "+",
        "linux": "-",
        "btw": ".",
        "the": "[",
        "way": "]",
        "i": "<",
        "use": ">"
    }
    
    bf_code = ""
    for token in tokens:
        if token in bf_mapping:
            bf_code += bf_mapping[token]
            
    # Trình biên dịch Brainfuck
    output = ""
    loop_stack = []
    loop_map = {}
    
    # Bước 1: Xây dựng bản đồ vòng lặp (Matching brackets)
    for i, char in enumerate(bf_code):
        if char == '[':
            loop_stack.append(i)
        elif char == ']':
            if loop_stack: # Kiểm tra stack để tránh lỗi nếu code sai cú pháp
                start = loop_stack.pop()
                loop_map[start] = i
                loop_map[i] = start
            
    # Bước 2: Thực thi
    pc = 0 # Program counter
    while pc < len(bf_code):
        cmd = bf_code[pc]
        
        if cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '.':
            output += chr(tape[ptr])
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = loop_map[pc]
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = loop_map[pc]
        
        pc += 1
        
    return output

# Nội dung file đầy đủ
content = """
arch arch arch arch arch arch
the linux i arch arch arch arch arch arch arch arch use way
i btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch arch arch arch arch btw
arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux btw
linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux btw
linux linux linux linux linux linux linux linux btw
linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
arch arch arch arch arch arch arch arch btw
linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux linux btw
arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch arch btw
"""

# Gọi hàm với tên biến đúng
print("Flag tìm được là:")
print(solve_arch(content))