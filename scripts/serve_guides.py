"""Serve site/ with Wowhead tooltips; optional rebuild from Markdown."""
from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BUILD_SCRIPT = ROOT / "scripts" / "build_guide_site.py"
DEFAULT_PORT = 8080


def build() -> None:
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="HTTP server for HTML guides (Wowhead tooltips)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--build", action="store_true", help="Rebuild site/ from guides/*.md before start")
    parser.add_argument("--open", action="store_true", help="Open index.html in default browser")
    args = parser.parse_args()

    if args.build or not (SITE / "index.html").exists():
        print("Building site/ …")
        build()

    if not SITE.is_dir():
        print(f"Missing folder: {SITE}", file=sys.stderr)
        sys.exit(1)

    os.chdir(SITE)

    handler = http.server.SimpleHTTPRequestHandler

    class QuietHandler(handler):
        def log_message(self, fmt: str, *log_args) -> None:
            if log_args and str(log_args[1]) != "200":
                super().log_message(fmt, *log_args)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", args.port), QuietHandler) as httpd:
        url = f"http://127.0.0.1:{args.port}/"
        print(f"Serving {SITE}")
        print(f"Guides: {url}")
        print("Stop: Ctrl+C or IntelliJ red square")
        if args.open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
