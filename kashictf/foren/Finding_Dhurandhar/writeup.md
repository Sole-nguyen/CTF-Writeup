# Finding Dhurandhar - CTF Challenge Writeup

## Challenge Overview

**Category:** Forensics  
**Difficulty:** Medium  
**Files:** `memory.dmp` (memory dump file)

## Challenge Description

We're given a memory dump from a Pakistani politician's machine that was cloned by RAW agent "Dhurandhar". The dump contains breadcrumbs left by another agent - the secret is split in two parts: one in network traffic and one in memory.

## Solution

### Step 1: Initial Analysis

First, examine the memory dump to understand its structure:

```bash
file memory.dmp
strings memory.dmp | head -200
```

The dump contains:
- Process information (System, notepad.exe, dhurandhar.exe, etc.)
- File references (flag.bin, dhurandhar_diary.txt, etc.)
- Registry artifacts
- Network capture data
- Embedded JPEG images

### Step 2: Finding the Clues

Searching through the strings reveals several important clues:

```
KEY_FRAGMENT_2=m a m u _ j a m a l i
```

And base64-encoded hints:
- `ZGh1cmFuZGhhcl9rYV9yYWF6X2hhaV95ZWg=` → `dhurandhar_ka_raaz_hai_yeh`
- `bHlhcmlfa2lfa2FoYW5pX3N1bm9nZQ==` → `lyari_ki_kahani_sunoge`

The dump also contains:
```
Combine karo dono hisson ko aur steghide chalao flag.bin par.
```
(Translation: "Combine both parts and run steghide on flag.bin")

### Step 3: Carving Embedded Files

The dump contains two embedded files we need to extract:

#### 3.1 Extract capture.pcap

Located between PCAP magic bytes (`d4c3b2a1`) and the marker `NETWORK CAPTURE DATA END`:

```python
pcap_offset = dump_data.find(bytes.fromhex('d4c3b2a1'))
pcap_end = dump_data.find(b'NETWORK CAPTURE DATA END')
pcap_data = dump_data[pcap_offset:pcap_end]
```

#### 3.2 Extract flag.bin

The second JPEG in the dump (the first is dhurandhar_photo.dat):

```python
jpg_sig = b'\xff\xd8\xff\xe0'  # JPEG/JFIF signature
# Find second occurrence
jpg_start = [second occurrence]
jpg_end = dump_data.find(b'\xff\xd9', jpg_start) + 2  # JPEG end marker
flag_bin = dump_data[jpg_start:jpg_end]
```

### Step 4: Finding KEY_FRAGMENT_1

Analyzing the carved `capture.pcap` reveals base64-encoded data in the network traffic:

```
cmVhbF9kaHVyYW5kaGFyX29mX2x5YXJpX2lzXw==
```

Decoding this gives us:
```
real_dhurandhar_of_lyari_is_
```

This is **KEY_FRAGMENT_1** (the first half of the password).

### Step 5: Finding KEY_FRAGMENT_2

Looking at the memory dump around the marker `KEY_FRAGMENT_2=`, we find the text with spaces:

```
KEY_FRAGMENT_2=m a m u _ j a m a l i
```

Removing spaces gives us: `mamu_jamali`

This is **KEY_FRAGMENT_2** (the second half of the password).

### Step 6: Extracting the Flag

Combine both fragments:
```
PASSWORD = real_dhurandhar_of_lyari_is_mamu_jamali
```

Use steghide to extract the hidden data from flag.bin:

```bash
steghide extract -sf flag.bin -p "real_dhurandhar_of_lyari_is_mamu_jamali"
```

This extracts `flag.txt` containing:

```
kashiCTF{arey_fikar_na_kar_baccha_hai_tu_mera_chal_aja_tujhe_fanta_pila_hun}
```

## Flag

```
kashiCTF{arey_fikar_na_kar_baccha_hai_tu_mera_chal_aja_tujhe_fanta_pila_hun}
```

## Tools Used

- `strings` - Extract printable strings from binary
- `python3` - Scripting for file carving and base64 decoding
- `steghide` - Steganography tool for extracting hidden data

## Key Insights

1. **Memory Forensics**: The challenge required analyzing a Windows memory dump structure
2. **File Carving**: Extracting embedded files (PCAP and JPEG) based on magic bytes
3. **Network Analysis**: The PCAP contained the first password fragment in base64
4. **Steganography**: The final flag was hidden in a JPEG using steghide
5. **Puzzle Assembly**: Combining clues from multiple sources (network + memory) to reconstruct the password

## Lessons Learned

- Always examine memory dumps thoroughly - they can contain multiple layers of hidden information
- Look for patterns like base64 encoding in binary data
- Network captures embedded in memory dumps can contain crucial information
- Steganography tools like steghide require exact passwords - attention to detail is critical
- CTF challenges often require combining multiple techniques (forensics, network analysis, steganography)
