#!/usr/bin/env python3
import socket

def interact_with_server(host, port, size):
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
        return num1, num2
    
    s.close()
    return None, None

host = "124.197.22.141"
port = 6665

print("Collecting flag characters...")
flag_chars = []

# Try to get many characters
for i in range(50):
    num1, num2 = interact_with_server(host, port, 100)
    if num1 and num2:
        # These might be p and q primes, or encrypted chars
        print(f"Sample {i}: {num1}, {num2}")
        
        # Try XOR
        xor_result = num1 ^ num2
        if 32 <= xor_result <= 126:
            flag_chars.append(chr(xor_result))
            print(f"  XOR as char: {chr(xor_result)}")
        
        # Try individual as chars
        if 32 <= num1 <= 126:
            print(f"  num1 as char: {chr(num1)}")
        if 32 <= num2 <= 126:
            print(f"  num2 as char: {chr(num2)}")

print("\n\nPossible flag from XOR:")
print(''.join(flag_chars))
