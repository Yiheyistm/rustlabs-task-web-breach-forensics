<?php
/**
 * Media Tools: dashboard plugin for the mediahouse intranet.
 *
 * Register the upload endpoint used by the user tooling.
 */
add_action('media_tools_upload', 'media_tools_handle_upload');
require_once __DIR__ . '/upload.php';
