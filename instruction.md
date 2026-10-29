# Server compromise — incident response engagement

You are the on-call responder for a small company whose web server shows
signs of compromise. The security team flagged the machine overnight and
wants a full assessment plus a clean handback before the morning traffic
window. A snapshot of the affected machine's state lives here (you are
inside the affected system). Investigate the machine the way an incident
responder would: logs, cron, systemd units, web roots, user homes, startup
hooks, running configuration — nothing is off-limits on this box.

## What happened (you must establish this)

An external actor broke in, gained privileged access, installed multiple
persistence mechanisms with a periodic command-and-control beacon, and left
droppers and shells behind. The customer's compliance team will only accept
a machine that is clean of attacker-controlled content.

## Deliverable 1 — the incident report

Write `/app/report.json` with EXACTLY this schema (extra keys are ignored;
missing keys or wrong types fail their checks):

```json
{
  "attacker_ip": "the single IP address the intruder operated from",
  "compromised_user": "the OS account first compromised by that actor",
  "initial_access": "one of: ssh_bruteforce | webshell_upload | malicious_package | phishing",
  "webshell_path": "absolute path of the uploaded web shell",
  "persistence": ["short names of every persistence mechanism you found"],
  "c2_host": "hostname the beacon connects to (from the encoded config)",
  "beacon_interval_minutes": 0,
  "privesc_or_payload_path": "absolute path of the downloaded stage-2 binary/script"
}
```

- `persistence` short names you should standardise on:
  `cron_beacon`, `systemd_service`, `ssh_authorized_key`, `web_shell`,
  `startup_script`.
- `beacon_interval_minutes` is the number of minutes between beacon runs.
- `compromised_user` is the account **the attacker first obtained**; the
  login chain may escalate further. Do not report root unless that is what
  the evidence shows — cite what the artifacts say.

## Deliverable 2 — make the box clean

Remove the attacker's foothold and persistence from this machine *for
real* (delete files, restore clean configs). After your work, the graded
state requirements are:

1. The web shell file is gone from the web root.
2. No crontab entry (root's crontab or any file under /etc/cron.d, /etc/cron.daily,
   /etc/cron.hourly) references the attacker's payload, domain, or encoded blob.
3. The malicious systemd unit file is gone and there is no symlink to it
   under /etc/systemd/system or /etc/systemd/system/*.wants.
4. The injected line is gone from every user's ~/.ssh/authorized_keys.
5. The stage-2 payload file the cron/unit references is gone.
6. There is no leftover file containing the attacker's encoded config blob
   referenced above anywhere on disk under /etc, /home, /root, /srv, /tmp,
   /var (search broadly — you'll know it when you see it).

Do NOT delete legitimate system state (real system cron files, the nginx
access log, the real config.php, the standard authorized_keys entries for
normal users).

## Artifact locations you may find useful

- `/var/log/nginx/access.log` — web traffic history
- `/var/log/auth.log` — SSH and sudo history
- `/var/www/html` — web root
- `/etc/cron.d`, `/etc/cron.daily`, `/etc/cron.hourly`, crontabs
- `/etc/systemd/system` and its `.wants/` subdirectories
- user home directories, `/root`, `/home`
- `/var/backups`

## Scoring

The verifier checks your report's facts against the true incident record
and re-scans the machine state you leave behind. Reward is the fraction of
graded checkpoints you satisfy. Report facts score even without cleanup
actions, and cleanup actions score even without a correct report: do both.
