#!/usr/bin/env python3
import socket

def get_char(host, port, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    # Read initial prompt
    s.recv(1024)
    
    # Send size
    s.send(f"{size}\n".encode())
    
    # Receive response
    response = s.recv(4096).decode()
    
    # Parse first two numbers
    lines = response.strip().split('\n')
    if len(lines) >= 2:
        num1 = int(lines[0])
        num2 = int(lines[1])
        s.close()
        return num2  # Return the second number as the character
    
    s.close()
    return None

host = "124.197.22.141"
port = 6665

print("Collecting flag...")
flag = []

# Get 100 characters to be safe
for i in range(100):
    char_code = get_char(host, port, 100)
    if char_code:
        if 32 <= char_code <= 126:
            char = chr(char_code)
            flag.append(char)
            print(char, end='', flush=True)
            
            # Check if we got the closing brace
            if char == '}':
                print("\n\nFlag found!")
                break
    else:
        print("?", end='', flush=True)

print("\n\nFull flag: " + ''.join(flag))
