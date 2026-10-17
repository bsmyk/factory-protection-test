import unittest

import app


class HomePage(unittest.TestCase):
    def test_has_welcome_heading(self):
        self.assertIn("<h1>Welcome</h1>", app.home_page(""))


class Greeting(unittest.TestCase):
    def test_named(self):
        self.assertIn("Hello, Ada!", app.home_page("name=Ada"))

    def test_default(self):
        self.assertIn("Hello, visitor!", app.home_page(""))

    def test_blank_name(self):
        self.assertIn("Hello, visitor!", app.home_page("name="))

    def test_plus_and_percent_encoding(self):
        self.assertIn("Hello, Ada Lovelace!", app.home_page("name=Ada+Lovelace"))
        self.assertIn("Hello, Ada Lovelace!", app.home_page("name=Ada%20Lovelace"))

    def test_keeps_heading(self):
        self.assertIn("<h1>Welcome</h1>", app.home_page("name=Ada"))


class Escaping(unittest.TestCase):
    def test_tags_escaped(self):
        page = app.home_page("name=%3Cb%3EAda%3C%2Fb%3E")
        self.assertIn("Hello, &lt;b&gt;Ada&lt;/b&gt;!", page)
        self.assertNotIn("<b>Ada</b>", page)

    def test_quotes_and_ampersand_escaped(self):
        self.assertIn("a&quot;b&amp;c", app.home_page("name=a%22b%26c"))

    def test_http_get_escaped(self):
        import threading
        import urllib.request
        from http.server import HTTPServer

        server = HTTPServer(("127.0.0.1", 0), app.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/?name=%3Cb%3EAda%3C/b%3E"
            with urllib.request.urlopen(url) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode()
                self.assertIn("&lt;b&gt;Ada&lt;/b&gt;", body)
                self.assertNotIn("<b>Ada</b>", body)
        finally:
            server.shutdown()
            server.server_close()


class HttpGreeting(unittest.TestCase):
    def test_get_with_name(self):
        import threading
        import urllib.request
        from http.server import HTTPServer

        server = HTTPServer(("127.0.0.1", 0), app.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/?name=Ada"
            with urllib.request.urlopen(url) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("Hello, Ada!", resp.read().decode())
        finally:
            server.shutdown()
            server.server_close()


class HealthCheck(unittest.TestCase):
    def get(self, path):
        import threading
        import urllib.error
        import urllib.request
        from http.server import HTTPServer

        server = HTTPServer(("127.0.0.1", 0), app.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}{path}") as resp:
                    return resp.status, resp.headers, resp.read()
            except urllib.error.HTTPError as err:
                return err.code, err.headers, err.read()
        finally:
            server.shutdown()
            server.server_close()

    def test_health(self):
        status, headers, body = self.get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"ok")
        self.assertTrue(headers["Content-Type"].startswith("text/plain"))
        self.assertEqual(headers["Content-Length"], "2")

    def test_health_with_query(self):
        status, _, body = self.get("/health?x=1")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"ok")

    def test_home_still_html(self):
        status, headers, body = self.get("/?name=Ada")
        self.assertEqual(status, 200)
        self.assertIn(b"Hello, Ada!", body)
        self.assertTrue(headers["Content-Type"].startswith("text/html"))

    def test_unknown_404(self):
        self.assertEqual(self.get("/nope")[0], 404)
