# Mahashamshan - Forensics Challenge Writeup

## Challenge Description

A packet capture was pulled from a compromised node inside a covert communications network. The operator left a cryptic note:

> "The river does not reveal itself. It only flows."
> 
> "Not all fields are what they seem. The fragment offset field hides more than offset."

We're warned that tools will lie, instincts will betray, and there are many ragebaits and fake helpers.

**Flag format**: `kashiCTF{...}`

## Initial Analysis

### Packet Overview

Opening the PCAP in Wireshark/tshark reveals:
- 216 total packets
- Mix of TCP, UDP, DNS, ICMP, and ARP traffic
- Multiple different source/destination IP pairs

```bash
$ tshark -r mahashamshan_2.pcap -q -z io,phs
```

The protocol hierarchy shows mostly TCP traffic with some DNS and ICMP packets.

### Identifying the Ragebaits

As warned, there are multiple decoys:

1. **ICMP Echo Requests** (192.168.7.77 → 1.1.1.1)
   - Contains hidden data in the ICMP payload
   - Extracting and ordering by sequence number reveals: `kashiCTF{1cm_echo_5t3g_f41l3d}`
   - This is a **fake flag** (ragебait)

2. **DNS Queries** to `telemetry.corp-internal.net`
   - Base64-encoded subdomains: `M19jMWR9`, `a2FzaGlDVEZ7`, `MF9zMzNfaDNy`, `bjB0aDFuZ190`
   - Decodes to: `3_c1d}kashiCTF{0_s33_h3rn0th1ng_t`
   - Another **fake flag fragment** (ragебait)

## Finding the Covert Channel

### The Key Clue

The challenge note mentions: *"The fragment offset field hides more than offset."*

Looking for packets with unusual fragment offset values:

```bash
$ tshark -r mahashamshan_2.pcap -Y "ip.frag_offset > 0" -T fields -e ip.src -e ip.dst -e ip.frag_offset
```

We find **41 packets** from `192.168.7.77` to `10.13.37.1` with:
- **Fragment offset = 40 bytes** (very unusual)
- **DF (Don't Fragment) flag SET** (contradictory!)
- **TTL = 33** (constant across all packets)

This combination is anomalous - you don't normally see DF set with a non-zero fragment offset.

### Packet Structure

Each covert packet has:
```
IP Header:
  - Src: 192.168.7.77
  - Dst: 10.13.37.1
  - TTL: 33 (0x21)
  - Fragment Offset: 40 bytes (5 units)
  - Flags: DF set
  
TCP-like Payload (not properly decoded due to fragment offset):
  - Contains what looks like TCP fields
  - SEQ field varies
  - Identical HTTP POST payload
```

## The Solution

### Step 1: Extract Covert Packets

Filter for the suspicious stream:

```python
from scapy.all import rdpcap, IP
import struct

packets = rdpcap('mahashamshan_2.pcap')
data = []

for pkt in packets:
    if IP in pkt:
        ip = pkt[IP]
        if ip.src == '192.168.7.77' and ip.dst == '10.13.37.1':
            # Extract TCP-like fields from payload
            payload = bytes(ip.payload)
            if len(payload) >= 20:
                sport, dport, seq, ack, off_flags, win, csum, urg = struct.unpack('!HHIIHHHH', payload[:20])
                data.append({
                    'ip_id': ip.id,
                    'ttl': ip.ttl,
                    'seq': seq
                })
```

This gives us 41 packets.

### Step 2: Determine Packet Ordering

The TCP SEQ field is the key to ordering! When we sort by SEQ value, patterns emerge:

```python
sorted_data = sorted(data, key=lambda x: x['seq'])
```

Looking at the IP ID high byte after sorting reveals a descending alphabet pattern, confirming the ordering is correct.

### Step 3: Extract the Hidden Data

The data is hidden in the **lower byte of the IP ID field**:

```python
lo_bytes = [d['ip_id'] & 0xFF for d in sorted_data]
```

Raw bytes (hex):
```
4a 40 52 49 48 62 75 67 5a 47 53 15 46 7e 43 10 ...
```

### Step 4: Decode with XOR

The TTL value (33 = 0x21) is the XOR key:

```python
ttl_key = 0x21
decoded = bytes([b ^ ttl_key for b in lo_bytes])
```

Result:
```
kashiCTF{fr4g_b1t5_4r3_my_5ecr3t_c4rr13r}
```

## Complete Solution

```python
from scapy.all import rdpcap, IP
import struct
import re

def extract_flag(pcap_file):
    packets = rdpcap(pcap_file)
    
    # Extract covert packets
    data = []
    for pkt in packets:
        if IP in pkt:
            ip = pkt[IP]
            if ip.src == '192.168.7.77' and ip.dst == '10.13.37.1':
                payload = bytes(ip.payload)
                if len(payload) >= 20:
                    seq = struct.unpack('!I', payload[4:8])[0]
                    data.append({'ip_id': ip.id, 'seq': seq})
    
    # Sort by SEQ field
    sorted_data = sorted(data, key=lambda x: x['seq'])
    
    # Extract lower byte of IP ID
    lo_bytes = [d['ip_id'] & 0xFF for d in sorted_data]
    
    # XOR with TTL (0x21)
    decoded = bytes([b ^ 0x21 for b in lo_bytes])
    
    # Extract flag
    flag = re.findall(rb'kashiCTF\{[^}]+\}', decoded)[0].decode()
    return flag

flag = extract_flag('mahashamshan_2.pcap')
print(f"FLAG: {flag}")
```

## Flag

```
kashiCTF{fr4g_b1t5_4r3_my_5ecr3t_c4rr13r}
```

## Key Takeaways

1. **Don't trust the obvious** - The ICMP and DNS flags were ragebaits
2. **Look for anomalies** - DF flag + non-zero fragment offset is contradictory
3. **Follow the clues** - "Fragment offset field hides more" pointed to the anomalous packets
4. **Packet ordering matters** - The SEQ field encoded the correct order
5. **Simple encoding** - Despite complexity, the final encoding was just XOR with TTL

The challenge name "Mahashamshan" (महाशमशान - great cremation ground in Sanskrit) hints at the need to look beyond surface-level deceptions to find the truth hidden beneath.
