import unittest
from urllib import urlopen
from nose.tools import assert_equals

class TestDecorator(unittest.TestCase):

    def test_should_minify_the_content_of_a_view_decorated(self):
        content = urlopen('http://localhost:8000/min').read()
        minified = '<!DOCTYPE html><html><body><p>Hello world! :D</p><div>Copyright 3000</div></body></html>'
        assert_equals(minified, content)

    def should_not_touch_the_content_of_an_undecorated_view(self):
        expected = '''
<html>
    <body>
        <p>Hello world! :D</p>
        <div>Copyright 3000</div>
    </body>
</html>
    '''
        content = urlopen('http://localhost:8000/raw').read()
        assert_equals(expected, content)
