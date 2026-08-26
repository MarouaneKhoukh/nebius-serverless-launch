#!/usr/bin/env bash
set -euo pipefail
python3 -m py_compile scripts/verify.py tests/test_verify.py tests/test_contract.py
python3 -m unittest discover -s tests -v
bash -n scripts/create_job.sh scripts/cleanup.sh scripts/check.sh
! grep 'AWS_SECRET_ACCESS_KEY=' README.md scripts/create_job.sh
