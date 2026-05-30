#!/usr/bin/env python3
import json

with open(r'C:\Users\duynh\Documents\Code\CTF\ASISCTF\Kiss_ASIS\interesting_samples.json') as f:
    data = json.load(f)

# Find samples with interesting GCDs
for s in data[:10]:
    g1 = s['gcd_N-1']
    g2 = s['gcd_N^2-1']
    if g1 > 1 or g2 > 1:
        k = s['k_estimate']
        print(f'Sample: k_est={k}')
        print(f'  gcd(e, N-1) = {g1}')
        print(f'  gcd(e, N^2-1) = {g2}')
        N = int(s['N'])
        e = int(s['e'])
        print(f'  N mod 9 = {N % 9}')
        print(f'  (N-1) mod 9 = {(N-1) % 9}')
        print(f'  e mod 9 = {e % 9}')
        print()
