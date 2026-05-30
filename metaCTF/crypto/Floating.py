import struct

data = b'\x8c\xae\xacA\xcf\x88j@\x06\x86\xcdD\xcc-\x86F\x0e\x8d\xeeC\xed\xac\x0e>,o\xecC\xaeFn>of\x8c>'

result = b''

for i in range(0, len(data), 4):
    chunk = data[i:i+4]
    
    # interpret as float
    f = struct.unpack("<f", chunk)[0]
    
    # reinterpret float as raw bytes again (double trick)
    result += struct.pack("<f", f)

print(result)
print(result.decode(errors="ignore"))
