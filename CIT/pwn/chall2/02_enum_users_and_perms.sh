#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
USER="${2:-greg}"

ssh -o StrictHostKeyChecking=no "$USER@$TARGET" <<'EOF'
echo "[*] users"
getent passwd | egrep 'greg|jimbo'

echo
echo "[*] check home of jimbo"
ls -ld /home/jimbo
ls -la /home/jimbo 2>&1 | head

echo
echo "[*] direct read attempt"
cat /home/jimbo/flag2.txt 2>&1 | head
EOF
