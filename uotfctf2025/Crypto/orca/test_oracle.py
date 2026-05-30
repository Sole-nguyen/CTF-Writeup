#!/usr/bin/env python3
import socket
import base64

def test_oracle():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(("34.186.247.84", 5000))
    
    # Read initial prompt
    prompt = s.recv(1024)
    print(f"Prompt: {repr(prompt)}")
    
    # Try a simple query
    s.sendall(b"0\n")
    resp = s.recv(1024)
    print(f"Response: {repr(resp)}")
    
    # Try with data
    s.sendall(b"1:41414141\n")
    resp = s.recv(1024)
    print(f"Response with data: {repr(resp)}")
    
    s.close()

if __name__ == "__main__":
    test_oracle()
