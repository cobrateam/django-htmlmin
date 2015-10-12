# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.test.client import Client


class TestDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_should_minify_the_content_of_a_view_decorated(self):
        response = self.client.get('/min')
        minified = b'<html><head></head><body><p>Hello world! :D' + \
                   b'</p><div>Copyright 3000</div></body></html>'
        self.assertEquals(minified, response.content)

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
        self.assertEquals(expected, response.content)

    def test_minify_response_should_be_false_in_not_minified_views(self):
        response = self.client.get('/not_min')
        self.assertEquals(False, response.minify_response)
