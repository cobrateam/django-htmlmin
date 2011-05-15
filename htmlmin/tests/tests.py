import unittest

from htmlmin.minify import html_minify

class TestMinify(unittest.TestCase):

    def test_html_should_be_minified(self):
        html = "<html>   <body>some text here</body>    </html>"

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(html_minified, html_minify(html))
