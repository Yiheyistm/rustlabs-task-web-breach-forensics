#!/usr/bin/env python3
"""Grade the web-breach forensics task.

14 checkpoints: 8 report facts (answer key) + 6 live cleanup actions.
reward = passed / 14.
"""

import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = "/logs/verifier"
BLOB = ("IyEvYmluL2Jhc2gKIyB0ZWxlbWV0cnktc3luYyBpbnN0YWxsIGNvbmZpZyAtIEFVVE8g"
        "R0VORVJBVEVELCBETyBOT1QgRURJVApFTkRQT0lOVD10ZWxlbWV0cnktc3luYy5tZWRp"
        "YWhvdXNlLWNkbi5leGFtcGxlOjg0NDMKUFJPVE9DT0w9dWRwCklOVEVSVkFMPTE1CkFV"
        "VEg9TUgtN2YzZDQxYTBiZTJjNTZkOQpNQVhfSklUVEVSPTMKUkVUUllfQkFDS09GRj04"
        "Cg==")

detail = []


def norm_path(p):
    if not isinstance(p, str):
        return ""
    p = p.strip()
    p = re.sub(r"/+", "/", p)
    return p.rstrip("/") if len(p) > 1 else p


def check_report(report, key):
    """8 facts."""
    got = 0
    if str(report.get("attacker_ip", "")).strip() == key["attacker_ip"]:
        got += 1
    else:
        detail.append("report: attacker_ip mismatch "
                      f"({report.get('attacker_ip')!r})")
    if str(report.get("compromised_user", "")).strip().lower() == \
            key["compromised_user"]:
        got += 1
    else:
        detail.append(f"report: compromised_user mismatch "
                      f"({report.get('compromised_user')!r})")
    if str(report.get("initial_access", "")).strip().lower() == \
            key["initial_access"]:
        got += 1
    else:
        detail.append(f"report: initial_access mismatch")
    if norm_path(report.get("webshell_path")) == key["webshell_path"]:
        got += 1
    else:
        detail.append("report: webshell_path mismatch")
    pers = report.get("persistence")
    if isinstance(pers, list):
        names = {str(x).strip().lower() for x in pers}
        required = set(key["persistence_required"])
        if required <= names:
            got += 1
        else:
            detail.append(f"report: persistence missing {required - names}")
    else:
        detail.append("report: persistence not a list")
    if str(report.get("c2_host", "")).strip().lower().replace("http://", "") \
            .replace("https://", "") == key["c2_host"]:
        got += 1
    else:
        detail.append("report: c2_host mismatch")
    iv = report.get("beacon_interval_minutes")
    if isinstance(iv, int) and iv == key["beacon_interval_minutes"]:
        got += 1
    else:
        detail.append("report: beacon_interval_minutes mismatch")
    if norm_path(report.get("privesc_or_payload_path")) == \
            key["privesc_or_payload_path"]:
        got += 1
    else:
        detail.append("report: privesc_or_payload_path mismatch")
    return got


def exists(path):
    return os.path.exists(path) or os.path.islink(path)


def no_cron_refs():
    """No cron file (or crontab) references the payload/domain/blob."""
    roots = ["/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly",
             "/etc/cron.weekly", "/etc/cron.monthly",
             "/var/spool/cron", "/etc/anacrontab"]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for name in dirnames + filenames:
                path = os.path.join(dirpath, name)
                if not os.path.isfile(path) or os.path.islink(path):
                    continue
                try:
                    with open(path, "r", errors="ignore") as fh:
                        text = fh.read()
                except OSError:
                    continue
                if ".telemetry-agent" in text or BLOB[:40] in text:
                    return False
    return True


def no_unit_fs():
    """Unit file gone; nothing in /etc/systemd/system links/refs it."""
    if exists("/etc/systemd/system/raidsync.service"):
        return False
    for path in glob.glob("/etc/systemd/system/**", recursive=True):
        if os.path.islink(path) and "raidsync" in os.readlink(path):
            return False
        if os.path.isfile(path) and path.endswith(".service") \
                and "raidsync" in os.path.basename(path):
            return False
    return True


def authorized_keys_clean():
    bad = []
    for path in glob.glob("/home/*/.ssh/authorized_keys") + \
            glob.glob("/root/.ssh/authorized_keys"):
        with open(path, "r", errors="ignore") as fh:
            text = fh.read()
        if "dev-access@198.51.100.7" in text:
            bad.append(path)
    return not bad


def blob_scavenger_clean():
    """Stage-2 blob must be gone from state dirs. Logs are exempt."""
    roots = ["/etc", "/home", "/root", "/srv", "/tmp", "/opt", "/usr/local",
             "/var/spool", "/dev/shm"]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                path = os.path.join(dirpath, name)
                if os.path.islink(path):
                    continue
                try:
                    if os.path.getsize(path) > 4_000_000:
                        continue
                    with open(path, "r", errors="ignore") as fh:
                        if BLOB[:40] in fh.read():
                            return False
                except OSError:
                    continue
    return True


def check_actions():
    """6 live checks."""
    got = 0
    if not exists("/var/www/html/wp-content/uploads/media-tools/"
                  "dbresetcache.php"):
        got += 1
    else:
        detail.append("action: webshell still present")
    if not (exists("/etc/cron.d/telemetry-sync")) and no_cron_refs():
        got += 1
    else:
        detail.append("action: cron persistence remains")
    if no_unit_fs():
        got += 1
    else:
        detail.append("action: systemd persistence remains")
    if authorized_keys_clean():
        got += 1
    else:
        detail.append("action: attacker key remains")
    if not exists("/usr/local/lib/.telemetry-agent"):
        got += 1
    else:
        detail.append("action: payload binary remains")
    if blob_scavenger_clean():
        got += 1
    else:
        detail.append("action: encoded config blob remains on disk")
    return got


def main():
    passed = 0
    total = 14
    try:
        with open("/app/report.json") as fh:
            report = json.load(fh)
    except Exception as ex:  # noqa: BLE001
        detail.append(f"no valid /app/report.json: {ex}")
        report = {}
    passed += check_report(report, json.load(open(
        os.path.join(HERE, "hidden", "answer_key.json"))))
    passed += check_actions()

    reward = passed / total
    os.makedirs(LOGS, exist_ok=True)
    open(os.path.join(LOGS, "reward.txt"), "w").write(str(reward))
    # numeric-only reward.json (harbor's parser rejects string values);
    # diagnostics go to a separate file.
    json.dump({"reward": reward},
              open(os.path.join(LOGS, "reward.json"), "w"), indent=1)
    json.dump({"passed": passed, "total": total, "detail": detail},
              open(os.path.join(LOGS, "detail.json"), "w"), indent=1)
    print(f"reward={reward}")


if __name__ == "__main__":
    main()
