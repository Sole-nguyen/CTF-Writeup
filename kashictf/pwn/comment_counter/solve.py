#!/usr/bin/env python3
from pwn import *

HOST = '34.126.223.46'
PORT = 17537

def main():
    log.info(f"Connecting to {HOST}:{PORT}...")
    r = remote(HOST, PORT)

    # 1. Wait for the banner to finish printing before we start spamming
    log.info("Reading instructions...")
    r.recvuntil(b"3 seconds per comment.")
    
    # Clean up any lingering newlines in the buffer
    sleep(0.5)
    r.clean()

    # 2. Stream the numbers 1 through 1000
    log.info("Starting the count: 1 to 1000...")
    for i in range(1, 1001):
        r.sendline(str(i).encode('utf-8'))
        
        # Log progress every 100 numbers so we don't spam our own terminal
        if i % 100 == 0:
            log.info(f"Sent {i}/1000")

    # 3. Catch the flag!
    log.success("Finished counting! Waiting for the server's response...")
    
    try:
        # Use recvall to grab whatever the server outputs (the flag) before it drops the connection
        final_output = r.recvall(timeout=3).decode('utf-8')
        print("\n" + "="*30)
        print("SERVER RESPONSE:")
        print("="*30)
        print(final_output.strip())
        print("="*30 + "\n")
    except Exception as e:
        log.warning("Did not get an EOF. Dropping to interactive mode...")
        r.interactive()

if __name__ == '__main__':
    main()
