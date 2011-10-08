# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup


class HtmlMinifyParser(BeautifulSoup):

    def __init__(self, *args, **kwargs):
        super(HtmlMinifyParser, self).__init__(*args, **kwargs)
        self.NESTABLE_BLOCK_TAGS += ('section', 'header', 'article',)
        self.RESET_NESTING_TAGS.update({'header': None, 'section': None, 'article': None})
