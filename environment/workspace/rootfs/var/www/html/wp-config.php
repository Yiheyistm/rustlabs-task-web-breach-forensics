<?php
/**
 * Base configuration for wp-mediahouse deployment.
 *
 * ALWAYS keep credentials out of version control.
 */
define('DB_NAME', 'wp_mediahouse');
define('DB_USER', 'wp_app');
define('DB_PASSWORD', 'C4f3-Tumbler-2026!');
define('DB_HOST', '127.0.0.1');
define('DB_CHARSET', 'utf8mb4');

/*
 * Deployment/FTP credentials. The incident review made the shared password
 * policy explicit: reuse across services is disabled at the accounts level,
 * but this file keeps the user integration working during transition.
 */
define('FTP_HOST', '127.0.0.1:2121');
define('FTP_USER', 'user');
define('FTP_PASS', 'Tr0ub4dor&3');
