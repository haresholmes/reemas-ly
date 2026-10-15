#!/usr/bin/env python3
"""
AL REEMAS LOGO STUDIO — Dedicated Local Preview Server
Serves the 8 Minimalist Artist Logo Concepts independently on Port 3001.
"""

import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 3001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class LogoStudioHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def guess_type(self, path):
        if path.endswith('.svg'):
            return 'image/svg+xml'
        if path.endswith('.js'):
            return 'application/javascript; charset=utf-8'
        if path.endswith('.css'):
            return 'text/css; charset=utf-8'
        if path.endswith('.html'):
            return 'text/html; charset=utf-8'
        return super().guess_type(path)

def start_studio_server(preferred_port=3001, auto_open=True):
    port = preferred_port
    max_tries = 20

    for _ in range(max_tries):
        try:
            with http.server.ThreadingHTTPServer(("", port), LogoStudioHTTPHandler) as httpd:
                url = f"http://localhost:{port}"
                print("=" * 66)
                print("  AL REEMAS LOGO STUDIO — DEDICATED PREVIEW URL")
                print("  مختبر شعار الريماس الفني (36 مفهوماً مينيمال مرسوماً بريشة فنان)")
                print("=" * 66)
                print(f"  ➜ Studio URL:   {url}")
                print(f"  ➜ Directory:    {DIRECTORY}")
                print(f"  ➜ Status:       Ready & Serving (Multi-threaded)")
                print("-" * 66)
                print("  Press Ctrl+C to stop the studio server.")
                print("=" * 66)

                if auto_open:
                    webbrowser.open(url)

                httpd.serve_forever()
        except OSError as e:
            if e.errno == 48:
                port += 1
            else:
                raise e

if __name__ == '__main__':
    open_browser = '--open' in sys.argv or '-o' in sys.argv or True
    try:
        start_studio_server(preferred_port=PORT, auto_open=open_browser)
    except KeyboardInterrupt:
        print("\nStudio server stopped gracefully.")
        sys.exit(0)
