from htmlmin.minify import html_minify


class HtmlMinifyMiddleware(object):

    def process_response(self, request, response):
        if response['Content-Type'] == 'text/html':
            response.content = html_minify(response.content)
        return response


