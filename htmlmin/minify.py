# -*- coding: utf-8 -*-
# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from BeautifulSoup import Comment
from parser import HtmlMinifyParser
from util import force_decode, between_two_tags

EXCLUDE_TAGS = ('pre', 'script', 'textarea',)

TAGS_PATTERN = '############ %s %d ############'


def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)
    soup = HtmlMinifyParser(html_code)
    exclude_tags = {}

    for tag in EXCLUDE_TAGS:
        exclude_tags[tag] = [str(script) for script in soup.findAll(name=tag) if len(script.text) > 0]

        for index, script in enumerate(exclude_tags[tag]):
            html_code = html_code.replace(script.decode('utf-8'), TAGS_PATTERN % (tag, index))

    soup = HtmlMinifyParser(html_code)

    if ignore_comments:
        [comment.extract() for comment in soup.findAll(text=lambda text:isinstance(text, Comment))]

    html_code = str(soup)
    lines = html_code.split('\n')
    minified_lines = []

    for index, line in enumerate(lines):
        minified_line = line.strip()

        # not in between two tags
        if not between_two_tags(minified_line, minified_lines, index):
            minified_line = ' %s' % minified_line

        minified_lines.append(str(minified_line))

    content = "".join(minified_lines)

    for tag in EXCLUDE_TAGS:
        for index, script in enumerate(exclude_tags[tag]):
            content = content.replace(TAGS_PATTERN % (tag, index), script)

    return content
