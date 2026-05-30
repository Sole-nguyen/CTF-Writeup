import socket
import time

host = '14.225.212.104'
port = 9999

s = socket.socket()
s.connect((host, port))
time.sleep(1)
s.recv(4096)  # welcome

# Use 9 bullets
for i in range(9):
    s.send(b'1\n')
    time.sleep(0.3)
    s.recv(4096)

# Now monster has 1 HP, we have 1 bullet left
# Try different inputs
test_values = [b'0\n', b'3\n', b'-1\n', b'999\n', b'\n', b'q\n', b'exit\n']

for val in test_values:
    print(f"Trying: {val.strip()}")
    s.send(val)
    time.sleep(0.5)
    resp = s.recv(4096).decode('utf-8', errors='ignore')
    if 'Congrats' in resp or 'VSL' in resp or 'flag' in resp.lower():
        print("FOUND IT!")
        print(resp)
        break
    if len(resp) > 100:
        print(resp[:200])
    print("---")
    
s.close()
