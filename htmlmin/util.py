# -*- coding: utf-8 -*-
# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


def force_decode(string, encoding="utf-8"):
    for c in (encoding, "utf-8", "latin-1"):
        try:
            return string.decode(c)
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass


def between_two_tags(current_line, all_lines):
    """
    We are only between two tags if the previous line does end with a > and
    the current line starts with a <.

    @current_line - string with current html line
    @all_lines - list of strings of hmtl lines upto but not including the
                 current line

    Note this function assumes all strings are stripped so it doesn't have to
    worry about leading or trailing whitespace.
    """
    if not all_lines:
        return False
    if not current_line.startswith('<'):
        return False
    return all_lines[-1].endswith('>')
