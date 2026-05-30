# CTF Writeup: Pork Lubber

**Author:** sole_f1t
**Category:** MISC

## 📜 Mô tả đề bài
> Arrr! In what U.S. state be the land-lubber who be given the subnet that includes the address 44.30.122.69, as be known by the crown's reckonin'?
> Respond with: RS{two-letter state abbreviation}
> You only have 5 attempts to solve this challenge!

## 🎯 Phân tích từ khóa
Đề bài được viết theo phong cách cướp biển với 3 manh mối cốt lõi:
1. **Target IP:** `44.30.122.69`
2. **"Land-lubber":** Từ lóng chỉ kẻ không quen đi biển/nghiệp dư. Trong ngữ cảnh mạng AMPRNet (dành cho dân Amateur Radio), đây là cú chơi chữ ám chỉ một tổ chức phi-nghiệp-dư (phi-amateur), tức là một tổ chức thương mại được nhượng quyền.
3. **"Crown's reckonin'":** Sổ sách của hoàng gia. Ám chỉ cơ sở dữ liệu đăng ký Internet chính thức của Bắc Mỹ (ARIN WHOIS registry).

---

## 🕵️ Quá trình giải quyết (Methodology)

### Bước 1: Tra cứu WHOIS cơ bản (The Bait)
Tra cứu WHOIS mặc định cho IP `44.30.122.69`:
```bash
whois 44.30.122.69
```
**Kết quả:**
* **Organization:** Amateur Radio Digital Communications (ARDC)
* **NetName:** AMPRNET (44.0.0.0/8)
* **StateProv:** CA (California)

Thử nộp flag `RS{CA}` nhưng **không chính xác**. 
*Lý do:* ARDC là tổ chức mẹ (Amateur), họ cấp phát lại (reassign) các dải IP nhỏ hơn cho người dùng cuối trên toàn thế giới. Tổ chức mẹ ở California không có nghĩa là người dùng thực sự cũng ở đó.

### Bước 2: Phân tích Geofeed (The Second Bait)
Trong bản ghi WHOIS của ARDC có để lại một đường link Geofeed: `https://portal.ampr.org/storage/geofeed.csv`. 
Sau khi tải file `geofeed.csv` và kiểm tra xem subnet nào chứa `44.30.122.69`:

```bash
cat geofeed.csv | grep 44.30.122
```
**Kết quả:** `44.30.122.0/24,US,New York,Rochester,`

Thử nộp flag `RS{NY}` nhưng **vẫn sai**. 
*Lý do:* Bảng geofeed nội bộ này không phải là "sổ sách của hoàng gia" (official registry) hoặc tổ chức tại NY không phải là "land-lubber" thực sự đang kiểm soát luồng định tuyến.

### Bước 3: Đào sâu vào BGP Routing (The Breakthrough)
Để biết thực thể nào thực sự đang "cầm" địa chỉ IP này trên Internet, tôi sử dụng **BGP Toolkit** (của Hurricane Electric) để kiểm tra bảng định tuyến toàn cầu.

**Tra cứu Origin AS cho tiền tố 44.30.122.69:**
* **Less Specific Announcement (Dải rộng):** `44.0.0.0/9` được công bố bởi **AS7377** (University of California San Diego).
* **Most Specific Announcement (Dải chi tiết nhất):** `44.30.122.0/24` được công bố bởi **AS54054** (Deteque).

Theo nguyên tắc **Longest Prefix Match** của giao thức BGP, router sẽ ưu tiên đường đi chi tiết nhất. Do đó, tổ chức thực sự quản lý IP `44.30.122.69` là **Deteque**.
Deteque là một công ty thương mại về an ninh mạng/chống thư rác -> Hoàn toàn khớp với manh mối **"Land-lubber"** (không thuộc hội vô tuyến nghiệp dư).

### Bước 4: Kiểm tra sổ sách chính thức ("Crown's reckonin'")
Sau khi xác định được mục tiêu là Deteque, tôi thực hiện tra cứu ARIN WHOIS cho AS54054 hoặc tìm kiếm hồ sơ công ty Deteque trên hệ thống ARIN.

**Kết quả tra cứu tổ chức Deteque:**
* **OrgName:** Deteque
* **City:** Ashburn
* **StateProv:** VA
* **Country:** US

Tổ chức này đăng ký kinh doanh tại tiểu bang Virginia, có mã viết tắt là **VA**.

---

## 🚩 Kết luận
Bằng cách vượt qua các thông tin gây nhiễu từ block mạng mẹ (CA) và bảng geofeed nội bộ (NY), kết hợp với kỹ năng phân tích luồng định tuyến BGP để tìm ra origin AS thực sự (Deteque), chúng ta đã xác định được tiểu bang chính xác theo hồ sơ ARIN.

**Flag:** `RS{VA}`