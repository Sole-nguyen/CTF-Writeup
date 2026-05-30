#!/usr/bin/env python3
from pwn import *

HOST = '34.126.223.46'
PORT = 18190

def main():
    log.info(f"Connecting to {HOST}:{PORT}...")
    r = remote(HOST, PORT)

    # 1. Clear the banner
    log.info("Reading past the banner...")
    r.recvuntil(b"*********************************************")

    # 2. Strict loop for exactly 100 rounds
    for i in range(100):
        try:
            # Wait for the next question
            r.recvuntil(b'I GIVE: ')
            
            # Parse the number
            received_data = r.recvline().strip()
            number = int(received_data.decode('utf-8'))
            
            # Wait for the exact input prompt to stay synced
            r.recvuntil(b'YOU GIVE: ')
            
            # Calculate and send the answer
            answer = number + 10
            log.info(f"Round {i+1}/100 | Received: {number} -> Sending: {answer}")
            r.sendline(str(answer).encode('utf-8'))
            
        except EOFError:
            log.error(f"Server closed connection early on round {i+1}!")
            break
        except Exception as e:
            log.error(f"Encountered an issue: {e}")
            break

    # 3. Read the remaining output (the flag!)
    log.success("Finished 100 rounds! Grabbing the final server output...")
    try:
        # recvall() reads everything until the server hangs up
        final_output = r.recvall(timeout=5).decode('utf-8')
        
        print("\n" + "="*30)
        print("THE FLAG IS LIKELY BELOW:")
        print("="*30)
        print(final_output.strip())
        print("="*30 + "\n")
        
    except Exception as e:
        log.error(f"Failed to read final output: {e}")

if __name__ == '__main__':
    main()

