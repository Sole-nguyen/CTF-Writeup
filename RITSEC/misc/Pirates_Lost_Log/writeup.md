# Pirates Lost Log - Writeup
---

# CTF Writeup: The Legendary Pirate's Log

* **Category:** Misc
* **Target:** `linksnsec.stellasec.com`
* **Author:** sol3_f1t 
---

## 1. Phân tích thử thách (Challenge Overview)

Thử thách yêu cầu chúng ta tìm kiếm một "nhật ký hải tặc" được giấu trong các dòng chảy kỹ thuật số của hệ thống **DNS**. Các manh mối quan trọng bao gồm:
* **Domain gốc:** `linksnsec.stellasec.com`
* **Cơ chế:** Các mảnh vỡ được nối với nhau như một chuỗi xích (chain of clues).
* **Giao thức:** Chỉ chấp nhận **TCP** port 53.
* **Mục tiêu:** Tìm bản ghi **TXT** có nội dung dài nhất trong toàn bộ Zone.
* **Từ khóa gợi ý:** "nsec" (gợi ý về kỹ thuật DNSSEC Zone Walking).

---

## 2. Quá trình Trinh sát (Reconnaissance)

### Bước 1: Tìm máy chủ có thẩm quyền (Authoritative Name Server)
Sử dụng lệnh `dig` để tìm các Name Server quản lý domain `stellasec.com`:
```bash
dig NS stellasec.com
```
Kết quả cho thấy domain này được quản lý bởi `ns1.clickable.systems`. Tuy nhiên, khi kiểm tra sâu hơn vào subdomain mục tiêu:
```bash
dig NS linksnsec.stellasec.com
```
Ta phát hiện subdomain này được ủy quyền (delegate) cho một máy chủ riêng biệt: **`linksnsecns.stellasec.com`** (IP: `129.21.21.95`). Đây chính là nơi "kho báu" thực sự được cất giấu.

### Bước 2: Xác nhận rào cản TCP
Mọi truy vấn UDP thông thường đều bị timeout hoặc bị từ chối. Thử thách bắt buộc phải sử dụng flag `+tcp` để duy trì kết nối:
```bash
dig @linksnsecns.stellasec.com linksnsec.stellasec.com TXT +tcp
```

---

## 3. Khai thác (Exploitation)

### Kỹ thuật: DNSSEC Zone Walking
Trong hệ thống DNSSEC, bản ghi **NSEC (Next Secure)** được sử dụng để chứng minh một tên miền không tồn tại. Một bản ghi NSEC sẽ liệt kê tên miền hiện tại và tên miền **kế tiếp** theo thứ tự bảng chữ cái (canonical order) trong Zone đó.



Bằng cách truy vấn NSEC liên tục, ta có thể "đi bộ" (walking) qua toàn bộ Zone để liệt kê tất cả các subdomain ẩn mà không cần brute-force.

### Thực hiện thủ công (Manual Walk)
Truy vấn NSEC đầu tiên:
```bash
dig @linksnsecns.stellasec.com linksnsec.stellasec.com NSEC +tcp
```
Kết quả trả về:
`linksnsec.stellasec.com. NSEC 000n96.linksnsec.stellasec.com. NS SOA RRSIG NSEC DNSKEY`

Manh mối đầu tiên là subdomain **`000n96`**.

### Tự động hóa bằng Python (Automation)
Vì Zone này chứa rất nhiều subdomain (được đặt tên theo mã Hex 6 ký tự), việc thực hiện bằng tay rất tốn thời gian. Chúng ta sử dụng thư viện `dnspython` để tự động hóa quá trình "vét sạch" Zone.

```python
import dns.query
import dns.message
import dns.rdatatype

TARGET_NS = "129.21.21.95"  # linksnsecns.stellasec.com
START_DOMAIN = "linksnsec.stellasec.com"

def zone_walk():
    current_domain = START_DOMAIN
    all_fragments = []
    visited = set()

    while current_domain not in visited:
        visited.add(current_domain)
        
        # 1. Lấy mảnh vỡ TXT (Mảnh log)
        query_txt = dns.message.make_query(current_domain, dns.rdatatype.TXT)
        response_txt = dns.query.tcp(query_txt, TARGET_NS)
        for rrset in response_txt.answer:
            if rrset.rdtype == dns.rdatatype.TXT:
                for rdata in rrset:
                    all_fragments.append((current_domain, rdata.to_text().strip('"')))

        # 2. Tìm subdomain kế tiếp qua NSEC
        query_nsec = dns.message.make_query(current_domain, dns.rdatatype.NSEC)
        response_nsec = dns.query.tcp(query_nsec, TARGET_NS)
        next_domain = None
        for rrset in response_nsec.answer:
            if rrset.rdtype == dns.rdatatype.NSEC:
                next_domain = rrset[0].next.to_text().rstrip('.')
                break
        
        if not next_domain or next_domain == START_DOMAIN:
            break
        current_domain = next_domain

    # Tìm bản ghi dài nhất
    longest = max(all_fragments, key=lambda x: len(x[1]))
    print(f"Longest Record at {longest[0]}: {longest[1]}")

zone_walk()
```

---

## 4. Flag

Sau khi duyệt qua toàn bộ chuỗi NSEC, chúng ta tìm thấy bản ghi tại vị trí **`67ljie.linksnsec.stellasec.com`** nổi bật với độ dài **142 ký tự**, chứa nội dung của Flag.

> **Flag:**
> `RS{thebartentersawcaptainjackwalkintothebarwiththeshipswheelaroundhisnutsthebartenderaskedhimwhatwasgoingoncaptainjackrepliedyaaritsdrivingmenuts}`

---