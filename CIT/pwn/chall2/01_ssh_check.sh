#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-23.179.17.69}"
USER="${2:-greg}"

ssh -o StrictHostKeyChecking=no "$USER@$TARGET" <<'EOF'
whoami
id
pwd
ls -la ~
EOF
