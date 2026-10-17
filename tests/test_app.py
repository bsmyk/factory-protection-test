import unittest

import app


class HomePage(unittest.TestCase):
    def test_has_welcome_heading(self):
        self.assertIn("<h1>Welcome</h1>", app.home_page(""))
