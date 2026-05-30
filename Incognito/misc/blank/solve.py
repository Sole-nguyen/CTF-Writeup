data=open('blank.txt','rb').read().decode('ascii','ignore')
lines=data.splitlines()
ws=[[c for c in l if c in ' \t'] for l in lines]

def dec(chars):
    bits=''.join('1' if c=='\t' else '0' for c in chars)  # tab=1
    return bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8))

odd=b''.join(dec(ws[i]) for i in range(len(ws)) if i%2==0)   # 1-based odd
even=b''.join(dec(ws[i]) for i in range(len(ws)) if i%2==1)  # 1-based even
flag=bytes([odd[i]^even[i] for i in range(min(len(odd),len(even)))])
print(flag.decode())
