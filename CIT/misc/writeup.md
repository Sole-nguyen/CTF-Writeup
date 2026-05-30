# CIT Misc Writeup

## 1) dog_barks

**File:** `dog_barks/challenge.wav`  
**Ý tưởng:** Âm thanh tiếng chó sủa được mã hóa thành bit theo 2 mức (to/nhỏ), sau đó đổi sang ASCII.

### Cách làm
1. Dùng script có sẵn `dog_barks/solve.py` để tách từng tiếng sủa và lấy peak amplitude.
2. Nhận thấy chuỗi nhị phân thô chưa ra text đúng nếu decode trực tiếp.
3. Phân tích thêm theo tần số/dải tần của từng tiếng sủa:
   - Có nhóm tần số thấp và cao.
   - Có thêm dấu phân tách (separator) để chia thành từng byte 8 bit.
4. Decode từng block 8 bit theo mapping đúng và thu được flag.

### Flag
`CIT{b4rking_up_th3_wr0ng_tr33}`

---

## 2) whattheword

**File:** `whattheword/file`  
**Loại file:** Office encrypted container (OLE + `EncryptionInfo`, `EncryptedPackage`).

### Cách làm
1. Xác định đây là file Office bị mã hóa (AES/SHA512, spinCount 100000).
2. Trích hash bằng `office2john.py`:
   - Hash mode tương ứng MS Office 2013 (`hashcat -m 9600`).
3. Brute-force bằng wordlist phổ biến (`xato 100k`) với hashcat.
4. Crack được mật khẩu:
   - `q1w2e3r4t5`
5. Dùng `msoffcrypto-tool` giải mã file:
   - Thu được `docx`.
   - Trong document có ảnh `word/media/image1.png`.
6. Flag nằm trong nội dung ảnh theo đúng hint challenge.

### Thông tin quan trọng
- Password file: `q1w2e3r4t5`

### Flag
`CIT{b1rd_1s_th3_w0rd}`

