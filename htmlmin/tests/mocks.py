class ResponseMock(dict):

    def __init__(self, *args, **kwargs):
        super(ResponseMock, self).__init__(*args, **kwargs)
        self['Content-Type'] = 'text/html'

    status_code = 200
    content = "<html>   <body>some text here</body>    </html>"

