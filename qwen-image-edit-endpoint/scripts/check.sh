#!/usr/bin/env bash
set -euo pipefail
python3 -m py_compile scripts/verify.py tests/test_verify.py
python3 -m unittest discover -s tests -v
bash -n scripts/cleanup.sh scripts/check.sh
