"""A tiny web app: python3 app.py serves it on $PORT."""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def home_page(query: str) -> str:
    return "<!doctype html><title>Greeter</title><h1>Welcome</h1>"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path != "/":
            self.send_error(404)
            return
        body = home_page(query).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(os.environ.get("PORT", "8000"))), Handler).serve_forever()
