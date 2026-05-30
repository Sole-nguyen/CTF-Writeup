# Easy Forensics - CTF Writeup

## Challenge Information
- **Category:** Forensics
- **Difficulty:** Easy
- **Flag Format:** `kashiCTF{...}`

## Challenge Description
A network capture was obtained from an internal monitoring system after suspicious activity was detected. The traffic appears mostly benign, but analysts believe data was covertly exfiltrated during normal communication. No obvious file transfers are present. Your task is to analyze the capture and recover the hidden secret.

## Solution

### Step 1: Initial Analysis

First, I verified the file type:
```bash
file capture.pcap
```
Output confirmed it's a valid pcap capture file.

### Step 2: Examining Network Traffic

Using `tcpdump` to inspect the packets:
```bash
tcpdump -r capture.pcap -nn | head -50
```

This revealed interesting DNS traffic patterns:
- Multiple DNS A queries to domains like `NNQXG2DJINKE.exfil.internal`
- Mixed with legitimate-looking queries to `kashi.com` and `amazon.com`

The presence of **"exfil.internal"** domain immediately suggested DNS exfiltration!

### Step 3: Identifying the Exfiltration Technique

Key observations:
1. Suspicious subdomains with uppercase alphanumeric strings (NNQXG2DJINKE, M63ENZZV6ZLY, etc.)
2. These strings looked like **Base32 encoding** (uppercase A-Z and 2-7 characters)
3. Legitimate DNS queries were likely used as camouflage
4. All exfil queries were sent to `8.8.8.8` (Google DNS)

This is a classic **DNS tunneling** attack where data is encoded and hidden in DNS queries.

### Step 4: Extracting the Encoded Data

I extracted only the DNS queries to `exfil.internal`:
```bash
tcpdump -r capture.pcap -nn 2>/dev/null | \
  grep "exfil.internal" | \
  awk '{print $8}' | \
  sed 's/A?//' | \
  sed 's/.exfil.internal.//' | \
  tr -d ' '
```

This gave us the following subdomains:
```
NNQXG2DJINKE
M63ENZZV6ZLY
MZUWY5DSMF2G
S33OL5UXGX3T
NZSWC23ZPU
```

### Step 5: Decoding the Data

Concatenating all chunks together:
```
NNQXG2DJINKEM63ENZZV6ZLYMZUWY5DSMF2GS33OL5UXGX3TNZSWC23ZPU
```

Base32 decoding requires proper padding. I tried adding `=` padding characters:
```bash
echo "NNQXG2DJINKEM63ENZZV6ZLYMZUWY5DSMF2GS33OL5UXGX3TNZSWC23ZPU======" | base32 -d
```

### Step 6: Flag Retrieved! 🎉

```
kashiCTF{dns_exfiltration_is_sneaky}
```