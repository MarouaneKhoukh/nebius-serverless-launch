#!/usr/bin/env bash
set -euo pipefail

: "${JOB_ID:?Set JOB_ID to the exact Nebius job resource ID to delete}"
nebius ai job delete "$JOB_ID"
