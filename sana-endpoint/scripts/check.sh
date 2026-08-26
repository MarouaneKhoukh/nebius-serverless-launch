#!/usr/bin/env bash
set -euo pipefail
python3 -m py_compile serve.py scripts/verify.py tests/test_server.py tests/test_verify.py
python3 -m unittest discover -s tests -v
bash -n scripts/cleanup.sh scripts/check.sh
grep -q '^FROM pytorch/pytorch:2.13.0-cuda12.6-cudnn9-runtime$' Dockerfile
