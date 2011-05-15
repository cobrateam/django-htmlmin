import unittest

from htmlmin.minify import html_minify
from htmlmin.middleware import HtmlMinifyMiddleware


class TestMinify(unittest.TestCase):

    def test_html_should_be_minified(self):
        html = "<html>   <body>some text here</body>    </html>"

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(html_minified, html_minify(html))


class ResponseMock(object):

    _headers = {'content-type': ('Content Type', 'text/html')}
    content = "<html>   <body>some text here</body>    </html>"

class TestMiddleware(unittest.TestCase):

    def test_middleware_should_be_minify_response_when_mime_type_is_html(self):
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(None, response_mock)

        html_minified = "<html><body>some text here</body></html>"

        self.assertEqual(response.content, html_minified)

    def test_middleware_should_not_be_minify_response_when_mime_type_not_is_html(self):
        response_mock = ResponseMock()
        response_mock._headers['content-type'] = ('Content Type', 'application/json')
        response = HtmlMinifyMiddleware().process_response(None, response_mock)

        html_not_minified = "<html>   <body>some text here</body>    </html>"

        self.assertEqual(response.content, html_not_minified)
