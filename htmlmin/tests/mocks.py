class RequestMock(object):

    def __init__(self, path="/"):
        self.path = path

class ResponseMock(dict):

    def __init__(self, *args, **kwargs):
        super(ResponseMock, self).__init__(*args, **kwargs)
        self['Content-Type'] = 'text/html'

    status_code = 200
    content = "<html>   <body>some text here</body>    </html>"

class ResponseWithCommentMock(ResponseMock):
    content = "<html>   <!-- some comment --><body>some text here</body>    </html>"
