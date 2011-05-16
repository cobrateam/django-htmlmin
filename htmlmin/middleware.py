from htmlmin.minify import html_minify


class HtmlMinifyMiddleware(object):

    def process_response(self, request, response):
        if response.status_code == 200 and 'text/html' in response['Content-Type']:
            response.content = html_minify(response.content)
        return response
