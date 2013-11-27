# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class RequestMock(object):

    def __init__(self, path="/"):
        self.path = path
        self._hit_htmlmin = True


class RequestBareMock(object):

    def __init__(self, path="/"):
        self.path = path


class ResponseMock(dict):

    def __init__(self, *args, **kwargs):
        super(ResponseMock, self).__init__(*args, **kwargs)
        self['Content-Type'] = 'text/html'

    status_code = 200
    content = "<html>   <body>some text here</body>    </html>"


class ResponseWithCommentMock(ResponseMock):
    content = "<html>   <!-- some comment --><body>some " + \
              "text here</body>    </html>"
