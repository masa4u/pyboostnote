# -*- coding: utf-8 -*-
from boostnote.importer.base_impoter import BaseImpoter


class WikiImpoter(BaseImpoter):
    def __init__(self, wiki_root_url):
        self.wiki_root_url = wiki_root_url
        BaseImpoter.__init__(self)

