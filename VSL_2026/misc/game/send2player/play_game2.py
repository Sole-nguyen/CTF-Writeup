#!/usr/bin/env python3
import socket
import time
import sys

host = '14.225.212.104'
port = 9999

print(f'Connecting to {host}:{port}...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

try:
    s.connect((host, port))
    print('Connected!\n')
    
    # Receive initial data
    time.sleep(1)
    try:
        data = s.recv(8192).decode('utf-8', errors='ignore')
        print("=== Server Response ===")
        print(data)
        print("=======================\n")
    except socket.timeout:
        print("No initial data received\n")
    
    # Send choice 1 (gun) repeatedly
    for shot in range(1, 15):
        try:
            print(f"Sending choice 1 (shot {shot})...")
            s.send(b'1\n')
            time.sleep(0.5)
            
            data = s.recv(8192).decode('utf-8', errors='ignore')
            print(f"Response {shot}:")
            print(data)
            print("-" * 50)
            
            if not data:
                print("Connection closed by server")
                break
                
            if 'VSL' in data or 'flag' in data.lower() or 'Congrats' in data:
                print("\n!!! FOUND SOMETHING !!!")
                break
                
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"Connection error: {e}")
            break
        except socket.timeout:
            print("Timeout waiting for response")
            break
    
    s.close()
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
