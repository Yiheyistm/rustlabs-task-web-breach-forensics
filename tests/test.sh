#!/bin/bash
# Verifier for the web-breach forensics task (agent-invisible).
set -u
mkdir -p /logs/verifier
TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
timeout 900 python3 "$TESTS_DIR/compute_reward.py"
RC=$?
if [ $RC -ne 0 ] || [ ! -s /logs/verifier/reward.txt ]; then
    echo "verifier crashed (rc=$RC)" >&2
    echo 0.0 > /logs/verifier/reward.txt
    echo '{"reward": 0.0}' > /logs/verifier/reward.json
fi
echo "verifier finished rc=$RC reward=$(cat /logs/verifier/reward.txt 2>/dev/null)" >&2
