# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import sys
import unittest

from django.conf import settings
from htmlmin.middleware import HtmlMinifyMiddleware, MarkRequestMiddleware
from htmlmin.tests import TESTS_DIR
from htmlmin.tests.mocks import (RequestBareMock, RequestMock, ResponseMock,
                                 ResponseWithCommentMock)


class TestMiddleware(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, TESTS_DIR)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mock_settings'

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(TESTS_DIR)
        del os.environ['DJANGO_SETTINGS_MODULE']

    def test_should_minify_response_when_mime_type_is_html(self):
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )

        minified = "<html><head></head><body>some text here</body></html>"
        self.assertEqual(minified, response.content)

    def test_should_minify_with_any_charset(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'text/html; charset=utf-8'
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )

        minified = "<html><head></head><body>some text here</body></html>"
        self.assertEqual(minified, response.content)

    def test_should_not_minify_without_content(self):
        response_mock = ResponseMock()
        del response_mock['Content-Type']
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )

        html_not_minified = "<html>   <body>some text here</body>    </html>"
        self.assertEqual(html_not_minified, response.content)

    def test_should_not_minify_not_html_content(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'application/json'
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )

        html_not_minified = "<html>   <body>some text here</body>    </html>"
        self.assertEqual(html_not_minified, response.content)

    def test_should_not_minify_url_marked_as_not_minifiable(self):
        html_not_minified = "<html>   <body>some text here</body>    </html>"
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(
            RequestMock('/raw/'), response_mock,
        )
        self.assertEqual(html_not_minified, response.content)

    def test_should_minify_if_exclude_from_minifying_is_unset(self):
        old = settings.EXCLUDE_FROM_MINIFYING
        del settings.EXCLUDE_FROM_MINIFYING

        minified = "<html><head></head><body>some text here</body></html>"
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), ResponseMock(),
        )
        self.assertEqual(minified, response.content)

        settings.EXCLUDE_FROM_MINIFYING = old

    def test_should_not_minify_response_with_minify_response_false(self):
        html_not_minified = "<html>   <body>some text here</body>    </html>"
        response_mock = ResponseMock()
        response_mock.minify_response = False
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )
        self.assertEqual(html_not_minified, response.content)

    def test_should_minify_response_with_minify_response_true(self):
        minified = "<html><head></head><body>some text here</body></html>"
        response_mock = ResponseMock()
        response_mock.minify_response = True
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )
        self.assertEqual(minified, response.content)

    def test_should_keep_comments_when_they_are_enabled(self):
        old = settings.KEEP_COMMENTS_ON_MINIFYING
        settings.KEEP_COMMENTS_ON_MINIFYING = True

        minified = "<html><!-- some comment --><head></head><body>" + \
                   "some text here</body></html>"
        response_mock = ResponseWithCommentMock()
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )
        self.assertEqual(minified, response.content)

        settings.KEEP_COMMENTS_ON_MINIFYING = old

    def test_should_remove_comments_they_are_disabled(self):
        old = settings.KEEP_COMMENTS_ON_MINIFYING
        settings.KEEP_COMMENTS_ON_MINIFYING = False

        minified = "<html><head></head><body>some text here</body></html>"
        response_mock = ResponseWithCommentMock()
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )
        self.assertEqual(minified, response.content)

        settings.KEEP_COMMENTS_ON_MINIFYING = old

    def test_should_remove_comments_when_the_setting_is_not_specified(self):
        old = settings.KEEP_COMMENTS_ON_MINIFYING
        del settings.KEEP_COMMENTS_ON_MINIFYING

        minified = "<html><head></head><body>some text here</body></html>"
        response_mock = ResponseWithCommentMock()
        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), response_mock,
        )
        self.assertEqual(minified, response.content)

        settings.KEEP_COMMENTS_ON_MINIFYING = old

    def test_should_not_minify_if_the_HTML_MINIFY_setting_is_false(self):
        old = settings.HTML_MINIFY
        settings.HTML_MINIFY = False
        expected_output = "<html>   <body>some text here</body>    </html>"

        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), ResponseMock(),
        )
        self.assertEqual(expected_output, response.content)

        settings.HTML_MINIFY = old

    def test_should_not_minify_when_DEBUG_is_enabled(self):
        old = settings.HTML_MINIFY
        old_debug = settings.DEBUG
        del settings.HTML_MINIFY
        settings.DEBUG = True

        expected_output = "<html>   <body>some text here</body>    </html>"

        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), ResponseMock(),
        )
        self.assertEqual(expected_output, response.content)

        settings.DEBUG = old_debug
        settings.HTML_MINIFY = old

    def test_should_minify_when_DEBUG_is_false_and_MINIFY_is_unset(self):
        old = settings.HTML_MINIFY
        old_debug = settings.DEBUG
        del settings.HTML_MINIFY
        settings.DEBUG = False

        minified = "<html><head></head><body>some text here</body></html>"

        response = HtmlMinifyMiddleware().process_response(
            RequestMock(), ResponseMock(),
        )
        self.assertEqual(minified, response.content)

        settings.DEBUG = old_debug
        settings.HTML_MINIFY = old

    def test_should_set_flag_when_request_hits_middleware(self):
        request_mock = RequestBareMock()
        MarkRequestMiddleware().process_request(request_mock)
        self.assertTrue(request_mock._hit_htmlmin)

    def test_should_not_minify_when_request_did_not_hit_middleware(self):
        expected_output = "<html>   <body>some text here</body>    </html>"

        request_mock = RequestBareMock()
        response = HtmlMinifyMiddleware().process_response(
            request_mock, ResponseMock(),
        )
        self.assertEqual(expected_output, response.content)
