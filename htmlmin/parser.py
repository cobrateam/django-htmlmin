# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup


class HtmlMinifyParser(BeautifulSoup):

    def __init__(self, *args, **kwargs):
        super(HtmlMinifyParser, self).__init__(*args, **kwargs)
        html5_tags = ('section', 'header', 'article', 'menu', 'footer', 'nav', 'aside')
        self.NESTABLE_BLOCK_TAGS += html5_tags

        for tag in html5_tags:
            self.RESET_NESTING_TAGS[tag] = None
