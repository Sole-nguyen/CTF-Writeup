#!/usr/bin/env python3

import random
from pwn import *

def untemper(y):
    """Reverse the tempering transformation of MT19937"""
    y = int(y)
    
    # Reverse right shift by 18
    y ^= (y >> 18)
    
    # Reverse left shift by 15 with mask 0xEFC60000
    y ^= ((y << 15) & 0xEFC60000)
    
    # Reverse left shift by 7 with mask 0x9D2C5680
    y ^= ((y << 7) & 0x9D2C5680)
    y ^= ((y << 14) & 0x94284000)
    y ^= ((y << 28) & 0x10000000)
    
    # Reverse right shift by 11
    y ^= (y >> 11)
    y ^= (y >> 22)
    
    return y & 0xFFFFFFFF

def recover_state(outputs):
    """Recover MT19937 state from 624 consecutive outputs"""
    state = []
    for output in outputs:
        # Un-obfuscate by XORing with 0xCAFEBABE
        raw = output ^ 0xCAFEBABE
        # Untemper to get internal state value
        state_value = untemper(raw)
        state.append(state_value)
    return tuple(state + [624])

def main():
    # Connect to the challenge server
    host = "chall.0xfun.org"
    port = 33968
    
    conn = remote(host, port)
    
    # Receive initial prompt
    conn.recvuntil(b'>')
    
    # Collect 624 outputs by sending "spin" commands
    print("[*] Collecting 624 outputs from the server...")
    outputs = []
    
    for i in range(624):
        conn.sendline(b'spin')
        line = conn.recvline().decode().strip()
        if line.startswith('>'):
            line = line[1:].strip()
        if line.isdigit():
            outputs.append(int(line))
            if (i + 1) % 100 == 0:
                print(f"[*] Collected {i + 1} outputs...")
        conn.recvuntil(b'>')
    
    print(f"[*] Collected {len(outputs)} outputs")
    
    # Recover the MT state
    print("[*] Recovering Mersenne Twister state...")
    state = recover_state(outputs[:624])
    
    # Create a new Random object with the recovered state
    rng = random.Random()
    rng.setstate((3, state, None))
    
    # Skip forward to align with the server (we've already consumed 624 outputs)
    for _ in range(624):
        rng.getrandbits(32)
    
    # Now predict future values
    print("[*] State recovered! Predicting next values...")
    
    # Try to predict values
    success_count = 0
    for attempt in range(100):
        conn.sendline(b'predict')
        
        # Get the prompt asking for prediction
        response = conn.recvline().decode().strip()
        print(f"Server: {response}")
        
        # Predict the next value
        predicted_raw = rng.getrandbits(32)
        predicted_obfuscated = predicted_raw ^ 0xCAFEBABE
        print(f"[*] Sending prediction: {predicted_obfuscated}")
        conn.sendline(str(predicted_obfuscated).encode())
        
        # Get result
        result = conn.recvline().decode().strip()
        print(f"Result: {result}")
        
        if "correct" in result.lower() or "win" in result.lower():
            success_count += 1
        
        if "flag" in result.lower() or "0xfun{" in result:
            print(f"[+] Flag found: {result}")
            break
        
        # Check if there's more output
        try:
            conn.recvuntil(b'>', timeout=1)
        except:
            break
    
    print(f"[*] Successful predictions: {success_count}/{attempt + 1}")
    
    # Get any remaining output
    try:
        conn.interactive()
    except:
        pass
    
    conn.close()

if __name__ == "__main__":
    main()
