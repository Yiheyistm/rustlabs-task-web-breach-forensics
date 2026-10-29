#!/bin/bash
# Reference solution for the web-breach forensics task: full report + cleanup.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$DIR/files/report.json" /app/report.json

# remove web shell
rm -f /var/www/html/wp-content/uploads/media-tools/dbresetcache.php

# remove cron persistence (leave legitimate cron state untouched)
rm -f /etc/cron.d/telemetry-sync

# remove systemd unit and its enable symlink
rm -f /etc/systemd/system/raidsync.service
rm -f /etc/systemd/system/multi-user.target.wants/raidsync.service

# remove the attacker key line (keep legitimate keys)
sed -i '/dev-access@198\.51\.100\.7/d' /home/user/.ssh/authorized_keys

# remove the stage-2 payload and any regenerated state
rm -f /usr/local/lib/.telemetry-agent /dev/shm/.ts-conf

echo "cleanup complete"
