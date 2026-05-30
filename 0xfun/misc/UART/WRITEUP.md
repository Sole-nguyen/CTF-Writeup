# UART Challenge Writeup

## Challenge Information
- **Category:** Misc
- **Challenge:** UART
- **Flag Format:** `0xfun{}`

## Challenge Description
A strange transmission has been recorded. Something valuable lies within.

We're given a file: `uart.sr`

## Initial Analysis

### File Identification
```bash
$ file uart.sr
uart.sr: Zip archive data, at least v1.0 to extract, compression method=store
```

The `.sr` extension indicates this is a Sigrok session file - a logic analyzer capture format.

### Extracting the Archive
```bash
$ unzip -l uart.sr
Archive:  uart.sr
  Length      Date    Time    Name
---------  ---------- -----   ----
        1  2025-08-30 12:08   version
      148  2025-08-30 12:08   metadata
     2400  2025-08-30 12:08   logic-1-1
---------                     -------
     2549                     3 files
```

### Examining the Metadata
```bash
$ unzip -q uart.sr -d /tmp/uart && cat /tmp/uart/metadata

[global]
sigrok version=0.6.0-git-f06f788

[device 1]
capturefile=logic-1
total probes=1
samplerate=1 MHz
total analog=0
probe1=uart.ch1
unitsize=1
```

**Key Information:**
- Single channel capture (UART is single-wire for one direction)
- Sample rate: 1 MHz (1,000,000 samples per second)
- 2400 samples total
- File size: 2400 bytes (one byte per sample)

## Solution Approach

### Understanding UART Protocol
UART (Universal Asynchronous Receiver-Transmitter) is a serial communication protocol with:
- **Idle state:** Line is HIGH (1)
- **Start bit:** Line goes LOW (0) to signal start of transmission
- **Data bits:** Typically 8 bits, transmitted LSB (Least Significant Bit) first
- **Stop bit:** Line returns HIGH (1)

### Finding the Baud Rate

First, I analyzed the signal transitions to determine the bit period:

```python
# Find all transitions in the signal
transitions = []
for i in range(1, len(data)):
    if data[i] != data[i-1]:
        transitions.append(i)

# Calculate distances between transitions
distances = [transitions[i+1] - transitions[i] for i in range(len(transitions)-1)]
```

**Results:**
- Most common distance: **8 samples**
- Second most common: **9 samples**
- Third most common: **17 samples** (double bit period)

With a sample rate of 1 MHz and 8 samples per bit:
```
Baud Rate = Sample Rate / Samples per Bit
Baud Rate = 1,000,000 / 8 = 125,000 baud
```

### Decoding the UART Signal

I wrote a Python decoder that:
1. Scans for idle state (HIGH)
2. Detects start bit (HIGH → LOW transition)
3. Samples each of 8 data bits at the midpoint of the bit period
4. Reconstructs the byte (LSB first)
5. Moves to the next frame

```python
samples_per_bit = 8
decoded_bytes = []
i = 0

while i < len(bits):
    # Find idle (high)
    while i < len(bits) and bits[i] == 0:
        i += 1
    if i >= len(bits):
        break
    
    # Wait for start bit (falling edge)
    while i < len(bits) and bits[i] == 1:
        i += 1
    if i >= len(bits):
        break
    
    start_bit_pos = i
    
    # Read 8 data bits (LSB first)
    byte_val = 0
    for bit_num in range(8):
        sample_pos = start_bit_pos + samples_per_bit * (bit_num + 1) + samples_per_bit // 2
        if sample_pos >= len(bits):
            break
        bit_val = bits[sample_pos]
        byte_val |= (bit_val << bit_num)
    
    decoded_bytes.append(byte_val)
    i = start_bit_pos + samples_per_bit * 10  # Skip to next frame

result = bytes(decoded_bytes)
print(result.decode('ascii'))
```

### Result
```
0xfun{UART_82_M2_B392n9dn2}
```

## Flag
```
0xfun{UART_82_M2_B392n9dn2}
```

## Key Takeaways
1. **Sigrok files** are ZIP archives containing logic analyzer captures
2. **UART decoding** requires determining the baud rate from signal timing
3. **Sample rate analysis** helps identify bit periods by finding common transition distances
4. **UART transmits LSB first**, which is important for correct byte reconstruction
5. The baud rate of **125,000** is non-standard (common rates: 9600, 115200) but works with the 1 MHz sampling

## Tools Used
- Python 3 (custom UART decoder)
- Basic file utilities (unzip, hexdump)

## Alternative Approach
If Sigrok CLI tools are installed, you can decode directly:
```bash
sigrok-cli -i uart.sr -P uart:baudrate=125000:rx=uart.ch1 -A uart=ascii
```
