#!/usr/bin/env python3
"""
Simple HTTP server to preview the engineering slideshow
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8888
DIRECTORY = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}")
        print(f"📂 Serving files from: {DIRECTORY}")
        print(f"🎯 Direct link to slideshow: http://localhost:{PORT}/engineering_slideshow.html")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Automatically open the slideshow in default browser
        webbrowser.open(f"http://localhost:{PORT}/engineering_slideshow.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped")

if __name__ == "__main__":
    main()