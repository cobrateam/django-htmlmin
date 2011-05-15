import unittest

from htmlmin.middleware import HtmlMinifyMiddleware
from htmlmin.minify import html_minify
from os.path import abspath, dirname, join

resources_path = lambda *paths: abspath(join(dirname(__file__), 'resources', *paths))

class TestMinify(unittest.TestCase):

    def test_complete_html_should_be_minified(self):
        html_file = resources_path('with_menu.html')
        html_file_minified = resources_path('with_menu_minified.html')

        html = open(html_file).read()
        html_minified = open(html_file_minified).read().strip('\n')

        self.assertEqual(html_minified, html_minify(html))

    def test_html_with_blank_lines_should_be_minify(self):
        html_file = resources_path('with_blank_lines.html')
        html_file_minified = resources_path('with_blank_lines_minified.html')

        html = open(html_file).read()
        html_minified = open(html_file_minified).read().strip('\n')

        self.assertEqual(html_minified, html_minify(html))

    def test_html_should_be_minified(self):
        html = "<html>   <body>some text here</body>    </html>"

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(html_minified, html_minify(html))

class ResponseMock(dict):

    def __init__(self, *args, **kwargs):
        super(ResponseMock, self).__init__(*args, **kwargs)
        self['Content-Type'] = 'text/html'

    content = "<html>   <body>some text here</body>    </html>"

class TestMiddleware(unittest.TestCase):

    def test_middleware_should_be_minify_response_when_mime_type_is_html(self):
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(None, response_mock)

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(response.content, html_minified)

    def test_middleware_should_minify_with_any_charset(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'text/html; charset=utf-8'
        response = HtmlMinifyMiddleware().process_response(None, response_mock)

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(response.content, html_minified)

    def test_middleware_should_not_be_minify_response_when_mime_type_not_is_html(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'application/json'
        response = HtmlMinifyMiddleware().process_response(None, response_mock)

        html_not_minified = "<html>   <body>some text here</body>    </html>"

        self.assertEqual(response.content, html_not_minified)
