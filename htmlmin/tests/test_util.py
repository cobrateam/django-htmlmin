# -*- coding: utf-8 -*-

# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest
from htmlmin.util import force_decode, between_two_tags


class TestUtil(unittest.TestCase):

    def test_should_decode_a_utf8_string(self):
        string = "Blá blá"
        self.assertEqual(u"Blá blá", force_decode(string))

    def test_shoulde_decode_a_latin_string(self):
        unicode_object = "Blá blá".decode("utf-8").encode("latin-1")
        string = str(unicode_object)
        self.assertEqual(u"Blá blá", force_decode(string))

    def test_should_be_able_to_chose_the_encoding(self):
        ENCODING = 'IBM857'
        unicode_object = "Blá blá".decode("utf-8").encode(ENCODING)
        string = str(unicode_object)
        self.assertEqual(u"Blá blá", force_decode(string, encoding=ENCODING))

    def test_between_two_tags_works_on_first_line(self):
        between = between_two_tags('<html>', [])
        self.assertFalse(between)

    def test_between_two_tags_false_if_prev_line_has_no_tag_and_current_line_has_no_tag(self):
        between = between_two_tags('world', ['hello'])
        self.assertFalse(between)

    def test_between_two_tags_false_if_prev_line_has_tag_and_current_line_has_no_tag(self):
        between = between_two_tags('world', ['<p>hello</p>'])
        self.assertFalse(between)

    def test_between_two_tags_false_if_prev_line_has_no_tag_and_current_line_has_tag(self):
        between = between_two_tags('<a href="#">world</a>', ['hello'])
        self.assertFalse(between)

    def test_between_two_tags_true_if_prev_line_has_tag_and_current_line_has_tag(self):
        between = between_two_tags('<a href="#">world</a>', ['<p>hello</p>'])
        self.assertTrue(between)
