#!/usr/bin/env bash
set -euo pipefail
: "${JOB_ID:?Set JOB_ID to the Nebius job resource ID}"
nebius ai job delete "$JOB_ID"
