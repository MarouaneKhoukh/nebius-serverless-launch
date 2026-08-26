#!/usr/bin/env bash
set -euo pipefail

python3 -m py_compile scripts/verify.py tests/test_verify.py tests/test_contract.py
python3 -m unittest discover -s tests -v
bash -n scripts/create_job.sh scripts/cleanup.sh scripts/check.sh

if grep -E '(AWS_SECRET_ACCESS_KEY|HF_TOKEN)=[^[:space:]]+' \
  README.md .env.example scripts/create_job.sh scripts/cleanup.sh scripts/verify.py; then
  echo "A credential value appears to be committed." >&2
  exit 1
fi
