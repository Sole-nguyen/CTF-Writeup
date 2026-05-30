#!/usr/bin/env python3
import subprocess
import os
import zlib
import re

def get_ee_fe_indices():
    """Extract indices from ee/fe prefixed objects"""
    obj_files = []
    for root, dirs, files in os.walk('.git/objects'):
        for f in files:
            prefix = os.path.basename(root)
            if prefix and len(prefix) == 2:
                obj_hash = prefix + f
                obj_path = os.path.join(root, f)
                obj_files.append((obj_hash, obj_path))

    # Filter for ee/fe objects
    filtered = [(h, p) for h, p in obj_files if h.startswith('ee') or h.startswith('fe')]
    filtered.sort()

    indices = []
    for obj_hash, obj_path in filtered:
        with open(obj_path, 'rb') as f:
            raw_data = f.read()
            try:
                decompressed = zlib.decompress(raw_data)
                null_idx = decompressed.find(b'\x00')
                if null_idx != -1:
                    header = decompressed[:null_idx].decode('ascii')
                    content = decompressed[null_idx+1:]
                    obj_type, size = header.split()
                    
                    if obj_type in ['blob', 'commit']:
                        match = re.search(rb'(x = |commit )(\d+)', content)
                        if match:
                            value = int(match.group(2))
                            indices.append((obj_hash, value))
            except:
                pass

    # Sort by hash to maintain order
    indices.sort(key=lambda x: x[0])
    return indices

def get_all_blobs():
    """Get all blobs from the repository using git"""
    # Get all objects
    result = subprocess.run(['git', 'rev-list', '--all', '--objects'], 
                          capture_output=True, text=True, timeout=30)
    all_objects = [line.split()[0] for line in result.stdout.strip().split('\n') if line]
    
    # Filter for blobs and get their content
    blobs = []
    print(f"Processing {len(all_objects)} objects...")
    for i, obj in enumerate(all_objects):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(all_objects)}...")
        
        try:
            # Check type
            result = subprocess.run(['git', 'cat-file', '-t', obj], 
                                  capture_output=True, text=True, timeout=1)
            if result.stdout.strip() == 'blob':
                # Get content
                result = subprocess.run(['git', 'cat-file', '-p', obj], 
                                      capture_output=True, timeout=1)
                blobs.append((obj, result.stdout))
        except:
            pass
    
    return blobs

def main():
    print("="*60)
    print("Git CTF Flag Extractor")
    print("="*60)
    
    # Get indices from ee/fe objects
    print("\n[1] Extracting indices from ee/fe objects...")
    indices = get_ee_fe_indices()
    print(f"    Found {len(indices)} indices")
    for hash, idx in indices[:5]:
        print(f"      {hash[:8]}: {idx}")
    print(f"      ... and {len(indices)-5} more")
    
    # Get all blobs
    print("\n[2] Extracting all blobs from repository...")
    all_blobs = get_all_blobs()
    print(f"    Found {len(all_blobs)} blobs")
    
    # Extract flag
    print("\n[3] Extracting flag characters...")
    flag_chars = []
    for hash, idx in indices:
        if idx < len(all_blobs):
            blob_hash, blob_content = all_blobs[idx]
            if len(blob_content) > 0:
                char = chr(blob_content[0]) if blob_content[0] < 128 else '?'
                flag_chars.append(char)
                print(f"    Index {idx:3d}: '{char}'")
            else:
                flag_chars.append('?')
                print(f"    Index {idx:3d}: EMPTY")
        else:
            flag_chars.append('?')
            print(f"    Index {idx:3d}: OUT OF RANGE (max={len(all_blobs)})")
    
    flag = ''.join(flag_chars)
    print("\n" + "="*60)
    print(f"FLAG: {flag}")
    print("="*60)
    
    return flag

if __name__ == '__main__':
    main()
