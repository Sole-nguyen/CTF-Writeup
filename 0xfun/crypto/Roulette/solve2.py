#!/usr/bin/env python3

import socket
import random

def untemper(y):
    """Reverse the tempering transformation of MT19937"""
    y = int(y)
    
    # Reverse y ^= (y >> 11)
    y ^= (y >> 11)
    y ^= (y >> 22)
    
    # Reverse y ^= (y << 7) & 0x9D2C5680
    y ^= ((y << 7) & 0x9D2C5680)
    y ^= ((y << 14) & 0x94284000)
    y ^= ((y << 28) & 0x10000000)
    
    # Reverse y ^= (y << 15) & 0xEFC60000
    y ^= ((y << 15) & 0xEFC60000)
    
    # Reverse y ^= (y >> 18)
    y ^= (y >> 18)
    
    return y & 0xFFFFFFFF

def main():
    # Connect to the challenge server
    host = "chall.0xfun.org"
    port = 33968
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    print("[+] Connected to server")
    
    # Receive initial prompt
    data = sock.recv(1024).decode()
    print(f"Initial: {data}")
    
    # Collect 624 outputs by sending "spin" commands
    print("[*] Collecting 624 outputs from the server...")
    outputs = []
    
    for i in range(630):  # Request a bit more to be safe
        sock.send(b'spin\n')
        data = sock.recv(4096).decode().strip()
        
        # Extract all numbers from response
        for line in data.split('\n'):
            line = line.strip().lstrip('> ')
            if line.isdigit():
                outputs.append(int(line))
        
        if len(outputs) >= 624:
            break
        
        if (i + 1) % 100 == 0:
            print(f"[*] Collected {len(outputs)} outputs so far...")
    
    print(f"[*] Collected {len(outputs)} outputs")
    print(f"[*] First few: {outputs[:5]}")
    
    # Recover the MT state
    print("[*] Recovering Mersenne Twister state...")
    state = []
    for output in outputs[:624]:
        # Un-obfuscate by XORing with 0xCAFEBABE
        raw = output ^ 0xCAFEBABE
        # Untemper to get internal state value
        state_value = untemper(raw)
        state.append(state_value)
    
    # Create a new Random object with the recovered state
    rng = random.Random()
    rng.setstate((3, tuple(state + [624]), None))
    
    # Don't skip - the state we set should already be at position 624
    # meaning the next call will generate value 625
    
    # Now predict future values
    print("[*] State recovered! Predicting next values...")
    
    # Send predict command
    sock.send(b'predict\n')
    
    # Get the prompt - it will show us a value and then ask for 10 predictions
    data = sock.recv(4096).decode()
    print(f"Server response: {data}")
    
    # The server shows us the next value, so we need to consume one from our RNG
    # to stay aligned
    _ = rng.getrandbits(32)
    
    # Now predict the next 10 RAW values (before obfuscation)
    predictions = []
    for i in range(10):
        predicted_raw = rng.getrandbits(32)
        predictions.append(str(predicted_raw))
    
    prediction_string = " ".join(predictions)
    print(f"[*] Sending RAW predictions: {prediction_string}")
    sock.send(f"{prediction_string}\n".encode())
    
    # Get result
    sock.settimeout(5)
    try:
        result = sock.recv(4096).decode()
        print(f"\n[+] Result:\n{result}")
        
        if "flag" in result.lower() or "0xfun{" in result:
            print(f"[+] Flag found!")
    except Exception as e:
        print(f"Error: {e}")
    
    sock.close()

if __name__ == "__main__":
    main()
