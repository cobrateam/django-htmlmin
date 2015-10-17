# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re

from django.conf import settings
from htmlmin.minify import html_minify


class MarkRequestMiddleware(object):

    def process_request(self, request):
        request._hit_htmlmin = True


class HtmlMinifyMiddleware(object):

    def can_minify_response(self, request, response):
        try:
            req_ok = request._hit_htmlmin
        except AttributeError:
            return False
        else:
            if not req_ok:
                raise ValueError("`request._hit_htmlmin` was set to False, when should only be True or not set.")

        if hasattr(settings, 'EXCLUDE_FROM_MINIFYING'):
            for url_pattern in settings.EXCLUDE_FROM_MINIFYING:
                regex = re.compile(url_pattern)
                if regex.match(request.path.lstrip('/')):
                    return False

        resp_ok = response.status_code == 200
        resp_ok = resp_ok and 'text/html' in response.get('Content-Type', '')
        if hasattr(response, 'minify_response'):
            resp_ok = resp_ok and response.minify_response
        return resp_ok

    def process_response(self, request, response):
        minify = getattr(settings, "HTML_MINIFY", not settings.DEBUG)
        keep_comments = getattr(settings, 'KEEP_COMMENTS_ON_MINIFYING', False)
        parser = getattr(settings, 'HTML_MIN_PARSER', 'html5lib')
        if minify and self.can_minify_response(request, response):
            response.content = html_minify(response.content,
                                           ignore_comments=not keep_comments,
                                           parser=parser)
        return response
