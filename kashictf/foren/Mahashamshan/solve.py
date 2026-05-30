#!/usr/bin/env python3
"""
Mahashamshan - Covert Channel CTF Challenge Solver

The challenge hides data in packets with:
- Source: 192.168.7.77
- Destination: 10.13.37.1  
- Fragment offset: 40 bytes (unusual with DF flag set)
- TTL: 33 (0x21)

The key insight:
1. Filter covert packets by src/dst IPs
2. Sort by TCP SEQ field (encodes packet order)
3. Extract lower byte of IP ID field
4. XOR with TTL (0x21) to decode

Flag: kashiCTF{fr4g_b1t5_4r3_my_5ecr3t_c4rr13r}
"""

from scapy.all import rdpcap, IP
import struct
import re

def extract_covert_message(pcap_file):
    """Extract hidden message from covert channel packets"""
    
    packets = rdpcap(pcap_file)
    
    # Extract data from covert packets
    data = []
    for pkt in packets:
        if IP in pkt:
            ip = pkt[IP]
            # Filter for the covert communication stream
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
    
    print(f"[+] Found {len(data)} covert packets")
    
    # Sort by SEQ field - this is the packet ordering key!
    sorted_data = sorted(data, key=lambda x: x['seq'])
    print(f"[+] Sorted by TCP SEQ field")
    
    # Extract lower byte of IP ID from sorted packets
    lo_bytes = [d['ip_id'] & 0xFF for d in sorted_data]
    
    # The TTL is constant at 33 (0x21) - this is the XOR key
    ttl_key = 0x21
    
    # XOR to decode
    decoded = bytes([b ^ ttl_key for b in lo_bytes])
    
    print(f"[+] XORed with TTL value (0x{ttl_key:02x})")
    print(f"[+] Decoded: {decoded.decode('utf-8', errors='replace')}")
    
    # Extract flag
    flags = re.findall(rb'kashiCTF\{[^}]+\}', decoded)
    if flags:
        return flags[0].decode()
    
    return None

def main():
    pcap_file = 'mahashamshan_2.pcap?token=eyJ1c2VyX2lkIjoxMTUzLCJ0ZWFtX2lkIjo2MDgsImZpbGVfaWQiOjMzfQ.ac-Ajg.gpu5TDtZ-WcDH9y6OhSHqxLr09Y'
    
    print("="*60)
    print("Mahashamshan Covert Channel Solver")
    print("="*60)
    print()
    
    flag = extract_covert_message(pcap_file)
    
    if flag:
        print(f"\n{'='*60}")
        print(f"FLAG: {flag}")
        print(f"{'='*60}")
    else:
        print("\n[-] No flag found.")

if __name__ == '__main__':
    main()
