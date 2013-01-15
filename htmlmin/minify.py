# -*- coding: utf-8 -*-

# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re

import bs4

from .util import force_decode, between_two_tags

EXCLUDE_TAGS = ('pre', 'script', 'textarea',)

TAGS_PATTERN = '############ %s %d ############'


def html_minify(html_code, ignore_comments=True):
    html_code = force_decode(html_code)
    soup = bs4.BeautifulSoup(html_code, "html5lib")
    html_code = unicode(soup)
    exclude_tags = {}

    for tag in EXCLUDE_TAGS:
        exclude_tags[tag] = [unicode(e) for e in soup.findAll(name=tag) if len(e.text) > 0]

        for index, elem in enumerate(exclude_tags[tag]):
            html_code = html_code.replace(elem.decode('utf-8'), TAGS_PATTERN % (tag, index))

    soup = bs4.BeautifulSoup(html_code, "html5lib")

    if ignore_comments:
        [comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, bs4.Comment))]

    html_code = unicode(soup)
    lines = html_code.split('\n')
    minified_lines = []

    for index, line in enumerate(lines):
        minified_line = line.strip()

        # not in between two tags
        if not between_two_tags(minified_line, minified_lines, index):
            minified_line = ' %s' % minified_line

        minified_lines.append(unicode(minified_line))

    spaces_pattern = re.compile(r"\s+")
    content = "".join(minified_lines)
    content = spaces_pattern.sub(" ", content)

    for tag in EXCLUDE_TAGS:
        for index, script in enumerate(exclude_tags[tag]):
            content = content.replace(TAGS_PATTERN % (tag, index), script)

    return content
