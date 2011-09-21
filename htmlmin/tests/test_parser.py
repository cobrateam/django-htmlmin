# -*- coding: utf-8 -*-
import unittest

from htmlmin.parser import HtmlMinifyParser


class TestParser(unittest.TestCase):

    def test_should_be_able_to_nest_section_tag(self):
        parser = HtmlMinifyParser('<section><p><section></section></p></section>')
        assert 'section' in parser.NESTABLE_BLOCK_TAGS, '<section> should be nestable'

    def test_should_be_able_to_nest_header_tag(self):
        parser = HtmlMinifyParser('<section><p><section></section></p></section>')
        assert 'header' in parser.NESTABLE_BLOCK_TAGS, '<header> should be nestable'
