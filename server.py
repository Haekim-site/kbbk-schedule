#!/usr/bin/env python3
"""KBBK Schedule local server.
Serves static files and provides /ics endpoint that returns .ics with
Content-Disposition: inline so Safari opens Calendar directly (no download).
"""
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import sys

PORT = 8767
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/ics':
            params = parse_qs(parsed.query)
            ics = params.get('ics', [''])[0]
            body = ics.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/calendar; charset=utf-8')
            self.send_header('Content-Disposition', 'inline; filename="event.ics"')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("[kbbk] " + (fmt % args) + "\n")


if __name__ == '__main__':
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"KBBK Schedule serving on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
