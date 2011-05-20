import unittest
from htmlmin.minify import Cleaner
from nose.tools import assert_equals

class TestCleaner(unittest.TestCase):

    def setUp(self):
        self.cleaner = Cleaner()

    def test_should_remove_spaces_between_html_tags(self):
        input_code = '<html>    <head></head>    </html>'
        expected_output = '<html><head></head></html>'
        assert_equals(expected_output, self.cleaner.remove_spaces(input_code))

    def test_should_keep_one_space_inside_html_tags(self):
        input_code = '<html>    <head>        <body><p class="header">Hello world!</p></body></head>    </html>'
        expected_output = '<html><head><body><p class="header">Hello world!</p></head></html>'
        assert_equals(expected_output, self.cleaner.remove_spaces(input_code))

    def test_should_drop_comments_from_html(self):
        html = '<html><body><!-- comment with <!-- comment inside --></body></html>'
        expected = '<html><body></body></html>'
        self.assertEqual(expected, self.cleaner.drop_comments(html))
