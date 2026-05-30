#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"

echo "[*] Scan full TCP ports on $TARGET"
nmap -Pn -p- --min-rate 1500 --max-retries 2 "$TARGET"

echo
echo "[*] Service detection on discovered FTP port"
nmap -Pn -sV -sC -p 10921 "$TARGET"
