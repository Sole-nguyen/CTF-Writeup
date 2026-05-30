#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
PORT="${2:-10921}"

echo "[*] Banner check"
{ echo; sleep 1; } | nc -nv "$TARGET" "$PORT" || true

echo
echo "[*] Anonymous listing"
curl -sS --user anonymous:anonymous "ftp://$TARGET:$PORT/"

