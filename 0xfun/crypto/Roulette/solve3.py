#!/usr/bin/env python3

import socket
import random

def untemper(y):
    """
    Reverse the MT19937 tempering transformation.
    Reference: https://en.wikipedia.org/wiki/Mersenne_Twister
    """
    y = int(y)
    
    # Reverse y ^= (y >> 18)
    y ^= y >> 18
    
    # Reverse y ^= (y << 15) & 0xEFC60000
    y ^= (y << 15) & 0xEFC60000
    
    # Reverse y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 14) & 0x94284000
    y ^= (y << 28) & 0x10000000
    
    # Reverse y ^= (y >> 11)
    y ^= y >> 11
    y ^= y >> 22
    
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
    print(f"[*] First 5: {outputs[:5]}")
    print(f"[*] Last 5: {outputs[619:624]}")
    
    # Recover the MT state
    print("[*] Recovering Mersenne Twister state...")
    state = []
    for i, output in enumerate(outputs[:624]):
        # Un-obfuscate by XORing with 0xCAFEBABE
        raw = output ^ 0xCAFEBABE
        # Untemper to get internal state value
        state_value = untemper(raw)
        state.append(state_value)
    
    print(f"[*] Recovered {len(state)} state values")
    
    # Create a new Random object with the recovered state
    # The state tuple is (version, (state_array + [index]), None)
    # After consuming 624 values, the index should be 624 (ready to twist)
    rng = random.Random()
    rng.setstate((3, tuple(state + [624]), None))
    
    print("[*] State set successfully")
    
    # Now predict future values
    print("[*] Sending predict command...")
    sock.send(b'predict\n')
    
    # Get the full response - value + prompt
    import time
    time.sleep(0.5)  # Give server time to send full response
    data = sock.recv(4096).decode()
    print(f"Server full response: {repr(data)}")
    
    # Extract the shown value to verify our prediction
    shown_value = None
    for line in data.split('\n'):
        line = line.strip().lstrip('> ')
        if line.isdigit():
            shown_value = int(line)
            break
    
    if shown_value:
        print(f"[*] Server showed obfuscated value: {shown_value}")
        # Predict what this should be
        test_raw = rng.getrandbits(32)
        test_obfuscated = test_raw ^ 0xCAFEBABE
        print(f"[*] We predicted: {test_obfuscated} (raw: {test_raw})")
        if test_obfuscated == shown_value:
            print("[+] MATCH! State recovery successful!")
        else:
            print(f"[!] MISMATCH! Off by: {abs(test_obfuscated - shown_value)}")
    else:
        print("[!] Could not extract shown value from server")
        print(f"Data was: {data}")
    
    # Now predict the next 10 RAW values
    print("[*] Predicting next 10 raw values...")
    predictions = []
    for i in range(10):
        predicted_raw = rng.getrandbits(32)
        predictions.append(str(predicted_raw))
        if i < 3:
            print(f"  Prediction {i+1}: {predicted_raw}")
    
    prediction_string = " ".join(predictions)
    print(f"[*] Sending: {prediction_string[:100]}...")
    
    import time
    time.sleep(0.5)  # Small delay to ensure server is ready
    
    sock.send(f"{prediction_string}\n".encode())
    sock.send(b"\n")  # Extra newline just in case
    
    # Get result
    sock.settimeout(5)
    print("[*] Waiting for server response...")
    try:
        result = sock.recv(8192).decode()
        print(f"\n[+] Server response (length={len(result)}):\n{result}")
        print(f"\n[+] Server response (repr):\n{repr(result)}")
        
        if "flag" in result.lower() or "0xfun{" in result:
            print(f"\n[+] ===== FLAG FOUND! =====")
        elif "wrong" in result.lower():
            print("[!] Server says our predictions were wrong!")
        elif "correct" in result.lower() or "right" in result.lower():
            print("[+] Server accepted our predictions!")
    except Exception as e:
        print(f"Error: {e}")
    
    sock.close()

if __name__ == "__main__":
    main()
