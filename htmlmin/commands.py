# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import argparse
import os
from htmlmin.minify import html_minify

my_dir = os.getcwd()

def main():
    parser = argparse.ArgumentParser(description=u'Minify content of HTML files')
    parser.add_argument('filename', metavar='filename', type=str, nargs=1)
    parser.add_argument('--keep-comments', action='store_true')
    args = parser.parse_args()

    content = ""
    with open(os.path.join(my_dir, args.filename[0])) as html_file:
        content = html_file.read()

    print html_minify(content, ignore_comments=not args.keep_comments)
