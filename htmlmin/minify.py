# -*- coding: utf-8 -*-

# Copyright 2013 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re
import six
import bs4

from .util import force_text

EXCLUDE_TAGS = set(["pre", "script", "textarea"])
# element list coming from
# https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5/HTML5_element_list
# combining text-level semantics & edits
TEXT_FLOW = set(["a", "em", "strong", "small", "s", "cite", "q", "dfn", "abbr", "data", "time", "code", "var", "samp", "kbd", "sup", "sub", "i", "b", "u", "mark", "ruby", "rt", "rp", "bdi", "bdo", "span", "br", "wbr", "ins", "del"])

# fold the doctype element, if True then no newline is added after the
# doctype element. If False, a newline will be insterted
FOLD_DOCTYPE = True
re_space = six.u('((?=\\s)[^\xa0])')
re_multi_space = re.compile(re_space + '+', re.MULTILINE|re.UNICODE)
re_single_nl = re.compile(r'^\n$', re.MULTILINE|re.UNICODE)
re_only_space = re.compile(r'^' + re_space + r'+$', re.MULTILINE|re.UNICODE)
re_start_space = re.compile(r'^' + re_space + '+', re.MULTILINE|re.UNICODE)
re_end_space = re.compile(re_space + r'+$', re.MULTILINE|re.UNICODE)
# see http://en.wikipedia.org/wiki/Conditional_comment
re_cond_comment = re.compile(r'\[if .*\]>.*<!\[endif\]',
                             re.MULTILINE|re.DOTALL|re.UNICODE)
re_cond_comment_start_space = re.compile(r'(\[if .*\]>)\s+',
    re.MULTILINE|re.DOTALL|re.UNICODE)
re_cond_comment_end_space = re.compile(r'\s+(<!\[endif\])',
    re.MULTILINE|re.DOTALL|re.UNICODE)


def html_minify(html_code, ignore_comments=True, parser="html5lib"):
    html_code = force_text(html_code)
    soup = bs4.BeautifulSoup(html_code, parser)
    mini_soup = space_minify(soup, ignore_comments)
    if FOLD_DOCTYPE is True:
        # monkey patching to remove new line after doctype
        bs4.element.Doctype.SUFFIX = six.u('>')
    return six.text_type(mini_soup)


def space_minify(soup, ignore_comments=True):
    """recursive function to reduce space characters in html code.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    :param ignore_comments: whether or not to keep comments in the
                            result
    :type ignore_comments: bool
    """
    # if tag excluded from minification, just pass
    if str(soup.name) in EXCLUDE_TAGS:
        return

    # loop through childrens of this element
    if hasattr(soup, 'children'):
        for child in soup.children:
            space_minify(child, ignore_comments)

    # if the element is a string ...
    if is_navstr(soup):
        # ... but not a comment, CData, Doctype or others (see
        # bs4/element.py for list).
        if not is_prestr(soup):
            # reduce multiple space characters
            new_string = re_multi_space.sub(' ', soup.string)
            (prev_flow, next_flow) = is_inflow(soup)
            # if the string is in a flow of text, don't remove lone
            # spaces
            if prev_flow and next_flow:
                new_string = re_only_space.sub(' ', new_string)
            # else, remove spaces, they are between grouping, section,
            # metadata or other types of block
            else:
                new_string = re_only_space.sub('', new_string)
            # if the previous element is not text then remove leading
            # spaces
            if prev_flow:
                new_string = re_start_space.sub(' ', new_string)
            else:
                new_string = re_start_space.sub('', new_string)
            # if the previous element is not text then remove leading
            # spaces
            if next_flow:
                new_string = re_end_space.sub(' ', new_string)
            else:
                new_string = re_end_space.sub('', new_string)
            # bs4 sometimes add a lone newline in the body
            new_string = re_single_nl.sub('', new_string)
            soup.string.replace_with(new_string)
        # Conditional comment content is HTML code so it should be
        # minified
        elif is_cond_comment(soup):
            new_string = re_multi_space.sub(' ', soup.string)
            new_string = re_cond_comment_start_space.sub(r'\1',
                                                         new_string)
            new_string = re_cond_comment_end_space.sub(r'\1', new_string)
            new_comment = bs4.element.Comment(new_string)
            soup.string.replace_with(new_comment)
        # if ignore_comments is True and this is a comment but not a
        # conditional comment and
        elif ignore_comments == True and is_comment(soup):
            # remove the element
            soup.string.replace_with(six.u(''))
    return soup

def is_navstr(soup):
    """test whether an element is a NavigableString or not, return a
    boolean.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    """
    return isinstance(soup, bs4.element.NavigableString)

def is_prestr(soup):
    """test whether an element is a PreformattedString or not, return a
    boolean.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    """
    return isinstance(soup, bs4.element.PreformattedString)

def is_comment(soup):
    """test whether an element is a Comment, return a boolean.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    """
    return isinstance(soup, bs4.element.Comment) \
        and not re_cond_comment.search(soup.string)

def is_cond_comment(soup):
    """test whether an element is a conditional comment, return a
    boolean.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    """
    return isinstance(soup, bs4.element.Comment) \
        and re_cond_comment.search(soup.string)

def is_inflow(soup):
    """test whether an element belongs to a text flow, returns a tuple
    of two booleans describing the flow around the element. The first
    boolean represents the flow before the element, the second boolean
    represents the flow after the element.

    :param soup: a BeautifulSoup of the code to reduce
    :type soup: bs4.BeautifulSoup
    """
    if soup.previous_sibling is not None and \
        soup.previous_sibling.name in TEXT_FLOW:
        prev_flow = True
    else:
        prev_flow = False
    if soup.next_sibling is not None and \
        soup.next_sibling.name in TEXT_FLOW:
        next_flow = True
    else:
        next_flow = False

    return (prev_flow, next_flow)
