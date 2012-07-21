# -*- coding: utf-8 -*-
# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import re
import HTMLParser
from BeautifulSoup import NavigableString, DEFAULT_OUTPUT_ENCODING


def force_decode(string, encoding="utf-8"):
    for c in (encoding, "utf-8", "latin-1"):
        try:
            return string.decode(c)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass

def between_two_tags(current_line, all_lines, index):
    if current_line and not current_line.startswith('<') and not all_lines[index-1].endswith('>'):
        return False
    return True

def fix_conditional_comments(string):
    result = re.compile('<!--\[if (.*)](.*)!\[endif\]-->').match(string)
    if not result:
        return string
    encoded_string = result.group(2)
    parser = HTMLParser.HTMLParser()
    return string.replace(encoded_string, parser.unescape(encoded_string))

class ConditionalComment(NavigableString):
    def __str__(self, encoding=DEFAULT_OUTPUT_ENCODING):
        return "<!--[if %s<![endif]-->" % NavigableString.__str__(self, encoding)
