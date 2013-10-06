# -*- coding: utf-8 -*-

# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re

import bs4
 
from HTMLParser import HTMLParser 

from .util import force_decode, between_two_tags

EXCLUDE_TAGS = ("pre", "script", "textarea",)

TAGS_PATTERN = "<%s>%d</%s>"

cond_regex = re.compile(r"<!--\[if .*\]>.*<!\[endif\]-->")


def is_conditional_comment(text):
    return cond_regex.match(text)


def html_minify(html_code, ignore_comments=True, parser="html5lib"):
    html_code = force_decode(html_code)
    soup = bs4.BeautifulSoup(html_code, parser)
    html_code = unicode(soup)
    exclude_tags = {}

    for tag in EXCLUDE_TAGS:
        exclude_tags[tag] = [unicode(e) for e in soup.findAll(name=tag)
                             if len(e.text) > 0]

        for index, elem in enumerate(exclude_tags[tag]):
            html_code = html_code.replace(elem,
                                          TAGS_PATTERN % (tag, index, tag))

    soup = bs4.BeautifulSoup(html_code, parser)

    if ignore_comments:
        f = lambda text: isinstance(text, bs4.Comment) and not \
            cond_regex.match(text.output_ready())
        [comment.extract() for comment in soup.findAll(text=f)]

    html_code = unicode(soup)
    html_code = html_code.replace(" \n", " ")
    lines = html_code.split("\n")
    minified_lines = []

    for index, line in enumerate(lines):
        minified_line = line.strip()
        if not between_two_tags(minified_line, minified_lines, index):
            minified_line = " %s" % minified_line
        minified_lines.append(unicode(minified_line))
        if minified_line.endswith("</a>") and \
                not lines[index + 1].startswith("</body>"):
            minified_lines.append(u" ")

    spaces_pattern = re.compile(r"\s+")
    content = "".join(minified_lines)
    content = spaces_pattern.sub(" ", content)

    for tag in EXCLUDE_TAGS:
        for index, e in enumerate(exclude_tags[tag]):
            content = content.replace(TAGS_PATTERN % (tag, index, tag), HTMLParser().unescape(e))

    return content
