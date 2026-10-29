# Demonstrated compromise — first-responder brief

You have full-sudo access on this machine as root (same as production).

Reminder of what the security team flagged:

- A web request about the media-tools plugin ended with a PHP file landing
  inside `wp-content/uploads/`, and later requests show command usage.
- Within minutes of the web requests, an SSH session for a service account
  appears in auth.log with new sudo activity.
- The billing team's ad-hoc audit (July 13) believes there are at least two
  automatic "phone home" mechanisms on this box that nobody reinstalled for
  a long time and that do not appear in the infrastructure inventory.
- A developer key was found in an authorized_keys file that then was not
  traced back to anyone on the payroll.

Full deliverables, required report schema and explicit cleanup contract are
described in the task instructions you received with this machine
(instruction.md at the task root). Fill your findings into
/app/report.json (a template is at /app/report.template.json).

Do not delete log files; they must stay for the postmortem.
