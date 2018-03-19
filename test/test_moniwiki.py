# -*- coding: utf-8 -*-

import unittest

from boostnote.migration.moniwiki import Moniwiki
from tempfile import TemporaryDirectory

class TestMoniwiki(unittest.TestCase):
    def setUp(self):
        self.wiki_url = 'https://wiki.kldp.org/wiki.php'
        self.target = TemporaryDirectory()

    def tearDown(self):
        pass

    def test_moniwiki_init(self):
        wiki = Moniwiki(self.wiki_url)
        wiki.do_import(self.target.name)
