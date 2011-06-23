from functools import wraps
from htmlmin.minify import html_minify

def minified_response(f):
    @wraps(f)
    def minify(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 200 and 'text/html' in response['Content-Type']:
            response.content = html_minify(response.content)
        return response

    return minify

def not_minified_response(f):
    @wraps(f)
    def not_minify(*args, **kwargs):
        response = f(*args, **kwargs)
        response.minify_response = False
        return response

    return not_minify