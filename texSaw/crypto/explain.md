# Giải thích Challenge Crypto

## Bước 1: Phân tích Ciphertext

Ciphertext sử dụng **Simple Substitution Cipher** - mỗi chữ cái được thay thế bởi một chữ cái khác cố định.

### Phương pháp giải:

1. **Frequency Analysis** - Phân tích tần suất xuất hiện:
   - Chữ 'z' xuất hiện nhiều nhất → có thể là 'e' hoặc 'o' trong tiếng Anh
   - Chữ 'n' xuất hiện nhiều → có thể là 'a' hoặc 'n'

2. **Pattern Recognition** - Nhận dạng mẫu:
   - "ugnu" xuất hiện nhiều lần → có thể là "that"
   - "nak" xuất hiện nhiều → có thể là "and"
   - "na" xuất hiện nhiều → có thể là "an" hoặc "in"
   - Chữ đơn "N" và "F" → có thể là "A" và "I"

3. **Building the mapping** (Xây dựng bảng chuyển đổi):
   - Từ "ugnu" = "that": u→t, g→h, n→a, u→t
   - Từ "nak" = "and": n→a, a→n, k→d
   - Từ "na" = "an": n→a, a→n
   - Tiếp tục với các pattern khác...

### Bảng chuyển đổi cuối cùng:
```
Cipher: a b c d e f g h i j k l m n o p q r s t u v w x y z
Plain:  n m l k j i h g f ? d c b a ? y z w v u t s r x p o
```

## Bước 2: Decoded Text

Sau khi giải mã, ta được văn bản:
"Noon rings out. A wasp, making an ominous sound, a sound akin to a klazon or a tocsin, flits about. Augustus, who has had a bad night..."

### Đặc điểm quan trọng:
- ❗ Văn bản KHÔNG có chữ 'e' nào cả!
- Đây là **Lipogram** - một kiểu văn học viết thiếu một chữ cái nhất định
- Nhân vật: Augustus
- Phong cách viết rất đặc biệt và phức tạp

## Bước 3: OSINT - Tìm tác giả

### Phương pháp tìm kiếm:

1. **Google Search** với các cụm từ đặc trưng:
   - "Augustus bad night lipogram"
   - "Noon rings out wasp"
   - "lipogram without letter e"

2. **GitHub Code Search** (quan trọng!):
   - Tìm exact phrases: "whirlwind of a cord" "whiplash of a cord"
   - Kết quả tìm thấy: Repository "BritishNationalCipherChallenge"
   
3. **Kiểm tra repository**:
   - Owner: themaddoctor
   - Path: 2001/4/plaintext.txt
   - File: solution.txt có thông tin về tác giả

### Kết quả tìm được:

File `solution.txt` cho biết:
```
The plaintext is from A Void, translated from Georges Perec's
La Disparition into English by Gilbert Adair.
```

## Tóm tắt:

1. **Văn bản gốc**: "La Disparition" (1969) - Georges Perec (tiếng Pháp)
2. **Bản dịch tiếng Anh**: "A Void" (1994) - Gilbert Adair
3. **Cipher**: Từ British National Cipher Challenge 2001

### Các tác giả liên quan:
- **Georges Perec** - tác giả gốc (tiếng Pháp)
- **Gilbert Adair** - người dịch sang tiếng Anh
- **themaddoctor** - người archive challenges lên GitHub

Tùy vào cách hiểu "original script", câu trả lời có thể là một trong các tên trên.
