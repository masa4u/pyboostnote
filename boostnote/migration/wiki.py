# -*- coding: utf-8 -*-
from boostnote.migration.migration_base import MigrationBase


class MigrationWiki(MigrationBase):
    def __init__(self, wiki_root_url):
        self.wiki_root_url = wiki_root_url
        MigrationBase.__init__(self)

