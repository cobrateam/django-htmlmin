# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re
from htmlmin.minify import html_minify
from django.conf import settings

class HtmlMinifyMiddleware(object):

    def can_minify_response(self, request, response):
        is_request_ok = True

        if hasattr(settings, 'EXCLUDE_FROM_MINIFYING'):
            for url_pattern in settings.EXCLUDE_FROM_MINIFYING:
                regex = re.compile(url_pattern)
                if regex.match(request.path.lstrip('/')):
                    is_request_ok = False
                    break

        is_response_ok = response.status_code == 200 and 'text/html' in response['Content-Type']
        if hasattr(response, 'minify_response'):
            is_response_ok = is_response_ok and response.minify_response
        return is_request_ok and is_response_ok

    def process_response(self, request, response):
        minify = getattr(settings, "HTML_MINIFY", not settings.DEBUG)
        keep_comments = getattr(settings, 'KEEP_COMMENTS_ON_MINIFYING', False)
        if minify and self.can_minify_response(request, response):
            response.content = html_minify(response.content, ignore_comments=not keep_comments)
        return response
