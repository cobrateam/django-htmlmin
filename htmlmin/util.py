# -*- coding: utf-8 -*-
# Copyright 2015 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import six


def force_text(s, encoding="utf-8"):
    if isinstance(s, six.text_type):
        return s
    try:
        if not isinstance(s, six.string_types):
            if six.PY3:
                if isinstance(s, bytes):
                    s = six.text_type(s, encoding)
                else:
                    s = six.text_type(s)
            elif hasattr(s, '__unicode__'):
                s = six.text_type(s)
            else:
                s = six.text_type(bytes(s), encoding)
        else:
            s = s.decode(encoding)
        return s
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass


def between_two_tags(current_line, all_lines, index):
    st = current_line and not current_line.startswith('<')
    if st and not all_lines[index - 1].endswith('>'):
        return False
    return True
