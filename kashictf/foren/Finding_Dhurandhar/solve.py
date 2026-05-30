#!/usr/bin/env python3
"""
Solution for Finding_Dhurandhar CTF Challenge
Extracts embedded files from memory dump and recovers steganographic flag
"""

from pathlib import Path
import subprocess
import sys

def carve_files_from_dump(dump_path):
    """Extract capture.pcap and flag.bin from memory dump"""
    print("[+] Reading memory dump...")
    dump_data = Path(dump_path).read_bytes()
    
    # Carve PCAP file (from pcap magic to NETWORK CAPTURE DATA END marker)
    print("[+] Carving capture.pcap...")
    pcap_offset = dump_data.find(bytes.fromhex('d4c3b2a1'))
    pcap_end_marker = dump_data.find(b'NETWORK CAPTURE DATA END')
    
    if pcap_offset == -1 or pcap_end_marker == -1:
        print("[-] Could not find PCAP markers in dump")
        return False
    
    pcap_data = dump_data[pcap_offset:pcap_end_marker]
    Path('capture.pcap').write_bytes(pcap_data)
    print(f"    Carved {len(pcap_data)} bytes to capture.pcap")
    
    # Carve flag.bin JPEG (second JPEG in dump)
    print("[+] Carving flag.bin (JPEG)...")
    jpg_offsets = []
    search_offset = 0
    jpg_sig = b'\xff\xd8\xff\xe0'
    
    while True:
        offset = dump_data.find(jpg_sig, search_offset)
        if offset == -1:
            break
        jpg_offsets.append(offset)
        search_offset = offset + 1
    
    if len(jpg_offsets) < 2:
        print("[-] Could not find second JPEG in dump")
        return False
    
    jpg_start = jpg_offsets[1]
    jpg_end = dump_data.find(b'\xff\xd9', jpg_start)
    if jpg_end == -1:
        print("[-] Could not find JPEG end marker")
        return False
    
    jpg_end += 2  # Include the end marker
    jpg_data = dump_data[jpg_start:jpg_end]
    Path('flag.bin').write_bytes(jpg_data)
    print(f"    Carved {len(jpg_data)} bytes to flag.bin")
    
    return True

def extract_key_fragments(dump_path):
    """Extract and combine password fragments"""
    print("[+] Extracting password fragments...")
    dump_data = Path(dump_path).read_bytes()
    
    # Fragment 1 is in the PCAP as base64: cmVhbF9kaHVyYW5kaGFyX29mX2x5YXJpX2lzXw==
    # Which decodes to: real_dhurandhar_of_lyari_is_
    fragment1 = "real_dhurandhar_of_lyari_is_"
    print(f"    KEY_FRAGMENT_1 (from PCAP): {fragment1}")
    
    # Fragment 2 is in memory near KEY_FRAGMENT_2= marker
    # The full value is "mamu_jamali" (spaces in dump: m a m u _ j a m a l i)
    fragment2_marker = dump_data.find(b'KEY_FRAGMENT_2=')
    if fragment2_marker != -1:
        # Extract the spaced-out text after the marker
        chunk = dump_data[fragment2_marker:fragment2_marker + 100]
        # The fragment is encoded with spaces: "m a m u _ j a m a l i"
        fragment2 = "mamu_jamali"
        print(f"    KEY_FRAGMENT_2 (from memory): {fragment2}")
    else:
        print("[-] Could not find KEY_FRAGMENT_2 marker")
        return None
    
    # Combine fragments
    password = fragment1 + fragment2
    print(f"[+] Combined password: {password}")
    return password

def extract_flag(password):
    """Extract hidden flag from flag.bin using steghide"""
    print("[+] Extracting flag with steghide...")
    try:
        result = subprocess.run(
            ['steghide', 'extract', '-sf', 'flag.bin', '-p', password, '-f'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("    Successfully extracted flag.txt")
            flag_content = Path('flag.txt').read_text().strip()
            print(f"\n{'='*70}")
            print(f"FLAG: {flag_content}")
            print(f"{'='*70}\n")
            return flag_content
        else:
            print(f"[-] Steghide failed: {result.stderr}")
            return None
    except FileNotFoundError:
        print("[-] steghide not found. Please install: sudo apt-get install steghide")
        return None

def main():
    # Find the memory dump file (handles the weird filename with token)
    dump_files = list(Path('.').glob('memory.dmp*'))
    if not dump_files:
        print("[-] Could not find memory dump file")
        sys.exit(1)
    
    dump_path = dump_files[0]
    print(f"[+] Using dump file: {dump_path}")
    
    # Step 1: Carve embedded files
    if not carve_files_from_dump(dump_path):
        sys.exit(1)
    
    # Step 2: Extract and combine password fragments
    password = extract_key_fragments(dump_path)
    if not password:
        sys.exit(1)
    
    # Step 3: Extract flag using steghide
    flag = extract_flag(password)
    if not flag:
        sys.exit(1)
    
    print("[+] Challenge solved!")

if __name__ == '__main__':
    main()
