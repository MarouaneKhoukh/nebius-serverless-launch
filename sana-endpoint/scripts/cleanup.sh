#!/usr/bin/env bash
set -euo pipefail
: "${ENDPOINT_ID:?Set ENDPOINT_ID to the Nebius endpoint resource ID}"
nebius ai endpoint delete "$ENDPOINT_ID"
