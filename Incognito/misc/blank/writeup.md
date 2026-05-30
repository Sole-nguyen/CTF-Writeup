# Blank (misc) — Writeup

## Ý tưởng
File `blank.txt` nhìn “trống” nhưng thực ra chứa **space/tab** có chủ đích. Ký tự `#` chỉ là mồi nhử (comment), còn dữ liệu nằm ở phần whitespace.

## Quan sát
Dùng `cat -A blank.txt` sẽ thấy rất nhiều `^I` (tab) và dấu `$` cuối dòng.
- Có 18 dòng.
- 16 dòng đầu có đúng **32 ký tự whitespace** (space/tab) mỗi dòng → rất hợp để mã hoá **32 bits = 4 bytes**.
- Các dòng chẵn (1-based) bắt đầu bằng `#`.

## Giải mã
Quy ước:
- `\t` (tab) = 1
- ` ` (space) = 0
- Ghép theo thứ tự xuất hiện, **MSB-first**, cứ 8 bit → 1 byte.

Kết quả:
- Ghép các **dòng chẵn** (1-based) → ra chuỗi ASCII lặp lại: `norickrollbro...` (đây là keystream).
- Ghép các **dòng lẻ** (1-based) → ra bytes “rác”.
- XOR hai chuỗi bytes (odd ⊕ even) → hiện plaintext chứa flag.

## Script (Python)
```py
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
```

## Flag
`IIITL{k1nda_ea5y_1t_w4s_br0_6767}`
