# -*- coding: utf-8 -*-

# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import unicode_literals

import codecs
import unittest
from os.path import abspath, dirname, join

import six

from htmlmin.minify import html_minify


def resources_path(*paths):
    return abspath(join(dirname(__file__), 'resources', *paths))


class TestMinify(unittest.TestCase):

    def _normal_and_minified(self, filename):
        html_file = resources_path('%s.html' % filename)
        html_file_minified = resources_path('%s_minified.html' % filename)

        html = open(html_file).read()
        f_minified = codecs.open(html_file_minified, encoding='utf-8')

        return html, f_minified.read().strip('\n')

    def test_complete_html_should_be_minified(self):
        html, minified = self._normal_and_minified('with_menu')
        self.assertEqual(minified, html_minify(html))

    def test_html_with_blank_lines_should_be_minify(self):
        html, minified = self._normal_and_minified('with_blank_lines')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_minify_content_from_script_tag(self):
        html, minified = self._normal_and_minified('with_javascript')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_convert_entity_the_content_of_script_tag(self):
        html, minified = self._normal_and_minified('with_html_content_in_javascript')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_minify_content_from_pre_tag(self):
        html, minified = self._normal_and_minified('with_pre')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_convert_entity_the_content_of_pre_tag(self):
        html, minified = self._normal_and_minified('with_html_content_in_pre')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_minify_content_from_textarea(self):
        html, minified = self._normal_and_minified('with_textarea')
        result = html_minify(html)
        self.assertEqual(minified, result)

    def test_should_convert_to_entities_the_content_of_textarea_tag(self):
        html, minified = self._normal_and_minified('with_html_content_in_textarea')
        result = html_minify(html)
        self.assertEqual(minified, result)

    def test_should_not_convert_entities_within_textarea_tag(self):
        html, minified = self._normal_and_minified('with_entities_in_textarea')
        result = html_minify(html)
        self.assertEqual(minified, result)

    def test_should_not_drop_blank_lines_from_the_begin_of_a_textarea(self):
        t = 'with_textarea_with_blank_lines'
        html, minified = self._normal_and_minified(t)
        result = html_minify(html)
        self.assertEqual(minified, result)

    def test_html_should_be_minified(self):
        html = "<html>   <body>some text here</body>    </html>"
        minified = "<html><head></head><body>some text here</body></html>"
        self.assertEqual(minified, html_minify(html))

    def test_minify_function_should_return_a_unicode_object(self):
        html = "<html>   <body>some text here</body>    </html>"
        minified = html_minify(html)
        if six.PY2:
            self.assertEqual(unicode, type(minified))
        else:
            self.assertEqual(str, type(minified))

    def test_minify_should_respect_encoding(self):
        html, minified = self._normal_and_minified('blogpost')
        self.assertEqual(minified, html_minify(html))

    def test_minify_should_not_prepend_doctype_when_its_not_present(self):
        html, minified = self._normal_and_minified('without_doctype')
        self.assertEqual(minified, html_minify(html))

    def test_minify_should_keep_doctype_when_its_present(self):
        html, minified = self._normal_and_minified('with_old_doctype')
        self.assertEqual(minified, html_minify(html))

    def test_should_exclude_comments_by_default(self):
        html, minified = self._normal_and_minified('with_comments_to_exclude')
        self.assertEqual(minified, html_minify(html))

    def test_should_be_able_to_not_exclude_comments(self):
        html, minified = self._normal_and_minified('with_comments')
        self.assertEqual(minified, html_minify(html, ignore_comments=False))

    def test_should_be_able_to_exclude_multiline_comments(self):
        t = 'with_multiple_line_comments'
        html, minified = self._normal_and_minified(t)
        self.assertEqual(minified, html_minify(html))

    def test_should_be_able_to_exclude_multiple_comments_on_a_page(self):
        html, minified = self._normal_and_minified('with_multiple_comments')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_exclude_conditional_comments(self):
        html, minified = self._normal_and_minified('with_conditional_comments')
        self.assertEqual(minified, html_minify(html))

    def test_should_not_rm_multiline_conditional_comments(self):
        html, minified = self._normal_and_minified('with_multiple_line_conditional_comments')
        self.assertEqual(minified, html_minify(html))

    def test_should_touch_attributes_only_on_tags(self):
        html = '<html>\n    <body>I selected you!</body>\n    </html>'
        minified = '<html><head></head><body>I selected you!</body></html>'
        self.assertEqual(minified, html_minify(html))

    def test_should_be_able_to_minify_html5_tags(self):
        html, minified = self._normal_and_minified('html5')
        self.assertEqual(minified, html_minify(html))

    def test_should_transform_multiple_spaces_in_one(self):
        html, minified = self._normal_and_minified('multiple_spaces')
        self.assertEqual(minified, html_minify(html))

    def test_should_convert_line_break_to_whitespace(self):
        html, minified = self._normal_and_minified('line_break')
        self.assertEqual(minified, html_minify(html))

    def test_should_keep_new_line_as_space_when_minifying(self):
        html = '<html><body>Click <a href="#">here</a>\nto see ' +\
               'more</body></html>'
        minified = '<html><head></head><body>Click <a href="#">here</a> to ' +\
                   'see more</body></html>'
        got_html = html_minify(html)
        self.assertEqual(minified, got_html)

    def test_should_not_produce_two_spaces_in_new_line(self):
        html = '<html><body>Click <a href="#">here</a> \nto see more' +\
               '</body></html>'
        minified = '<html><head></head><body>Click <a href="#">here' + \
                   '</a> to see more</body></html>'
        got_html = html_minify(html)
        self.assertEqual(minified, got_html)

    def test_should_keep_non_breaking_space(self):
        html = '<html><head></head><body>This is seperated&nbsp;by a non breaking space.</body></html>'
        minified = '<html><head></head><body>This is seperated\xa0by a non breaking space.</body></html>'
        got_html = html_minify(html)
        self.assertEqual(minified, got_html)

    def test_non_ascii(self):
        html, minified = self._normal_and_minified('non_ascii')
        self.assertEqual(minified, html_minify(html))

    def test_non_ascii_in_excluded_element(self):
        html, minified = self._normal_and_minified(
            'non_ascii_in_excluded_element'
        )
        self.assertEqual(minified, html_minify(html))
