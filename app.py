"""A tiny web app: python3 app.py serves it on $PORT."""
import html
import os
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer


def home_page(query: str) -> str:
    name = parse_qs(query).get("name", ["visitor"])[0]
    return f"<!doctype html><title>Greeter</title><h1>Welcome</h1><p>Hello, {html.escape(name, quote=True)}!</p>"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/health":
            body, content_type = b"ok", "text/plain; charset=utf-8"
        elif path == "/":
            body, content_type = home_page(query).encode(), "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(os.environ.get("PORT", "8000"))), Handler).serve_forever()
