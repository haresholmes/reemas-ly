#!/usr/bin/env python3
"""
AL REEMAS CENTER — Local Development & Preview Server
Zero-dependency HTTP server with automatic port detection and correct MIME types.
"""

import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ReemasHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and disable cache during development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def guess_type(self, path):
        mime_type = super().guess_type(path)
        if path.endswith('.svg'):
            return 'image/svg+xml'
        if path.endswith('.js'):
            return 'application/javascript; charset=utf-8'
        if path.endswith('.css'):
            return 'text/css; charset=utf-8'
        if path.endswith('.html'):
            return 'text/html; charset=utf-8'
        return mime_type

def start_server(preferred_port=3000, auto_open=False):
    port = preferred_port
    max_tries = 20

    for _ in range(max_tries):
        try:
            with socketserver.TCPServer(("", port), ReemasHTTPRequestHandler) as httpd:
                url = f"http://localhost:{port}"
                print("=" * 64)
                print("  AL REEMAS CENTER — LOCAL DEVELOPMENT SERVER")
                print("  مركز الريماس لاستيراد الذهب والمجوهرات")
                print("=" * 64)
                print(f"  ➜ Local URL:    {url}")
                print(f"  ➜ Root Dir:     {DIRECTORY}")
                print(f"  ➜ Language:     Arabic (RTL primary) ⇄ English (LTR)")
                print(f"  ➜ Status:       Ready & Serving")
                print("-" * 64)
                print("  Press Ctrl+C to stop the server.")
                print("=" * 64)

                if auto_open:
                    webbrowser.open(url)

                httpd.serve_forever()
        except OSError as e:
            if e.errno == 48:  # Address already in use
                port += 1
            else:
                raise e

if __name__ == '__main__':
    open_browser = '--open' in sys.argv or '-o' in sys.argv
    try:
        start_server(preferred_port=PORT, auto_open=open_browser)
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")
        sys.exit(0)
