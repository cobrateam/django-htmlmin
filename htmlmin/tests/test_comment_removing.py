import unittest
from htmlmin.minify import drop_comments

class TestCommentRemoving(unittest.TestCase):

    def test_nested_comments_should_also_be_excluded(self):
        html = '<html><body><!-- comment with <!-- comment inside --></body></html>'
        expected = '<html><body></body></html>'
        self.assertEqual(expected, drop_comments(html))
