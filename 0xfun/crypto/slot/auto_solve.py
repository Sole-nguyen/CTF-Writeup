#!/usr/bin/env python3
import socket

def solve_lcg(targets):
    M = 2147483647
    A = 48271
    C = 12345
    
    # Brute-force to find the state
    for k in range(M // 100 + 1):
        s1 = k * 100 + targets[0]
        s2 = (A * s1 + C) % M
        
        if s2 % 100 == targets[1]:
            current_state = s2
            match = True
            for i in range(2, len(targets)):
                current_state = (A * current_state + C) % M
                if current_state % 100 != targets[i]:
                    match = False
                    break
            
            if match:
                # Generate next 5 spins
                next_spins = []
                for _ in range(5):
                    current_state = (A * current_state + C) % M
                    next_spins.append(str(current_state % 100))
                
                return " ".join(next_spins)
    
    return None

def main():
    HOST = "chall.0xfun.org"
    PORT = 60723
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # Read the 10 spins
        data = b""
        while b"Predict the next 5 spins" not in data:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        
        print(data.decode())
        
        # Extract the spins
        lines = data.decode().strip().split('\n')
        spins = []
        for line in lines:
            line = line.strip()
            if line and line.isdigit():
                spins.append(int(line))
        
        print(f"Observed spins: {spins}")
        
        # Solve
        prediction = solve_lcg(spins)
        print(f"Prediction: {prediction}")
        
        # Send prediction
        s.sendall(prediction.encode() + b"\n")
        
        # Get response
        response = s.recv(4096)
        print(response.decode())

if __name__ == "__main__":
    main()
