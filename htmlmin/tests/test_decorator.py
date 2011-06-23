import unittest
from django.test.client import Client
from nose.tools import assert_equals

class TestDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_should_minify_the_content_of_a_view_decorated(self):
        response = self.client.get('/min')
        minified = '<!DOCTYPE html><html><body><p>Hello world! :D</p><div>Copyright 3000</div></body></html>'
        assert_equals(minified, response.content)

    def should_not_touch_the_content_of_an_undecorated_view(self):
        expected = '''
<html>
    <body>
        <p>Hello world! :D</p>
        <div>Copyright 3000</div>
    </body>
</html>
    '''
        response = self.client.get('/raw')
        assert_equals(expected, response.content)

    def test_should_set_minify_response_attribute_to_false_if_view_decorated_with_not_minified_response(self):
        response = self.client.get('/not_min')
        assert_equals(False, response.minify_response)
