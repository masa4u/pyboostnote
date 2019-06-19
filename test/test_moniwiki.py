# -*- coding: utf-8 -*-
import shutil
import unittest
from tempfile import mkdtemp

from boostnote.migration.moniwiki import Moniwiki


class TestMoniwiki(unittest.TestCase):
    def setUp(self):
        self.wiki_url = 'https://wiki.kldp.org/wiki.php'
        self.target = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.target)

    def test_moniwiki_init(self):
        wiki = Moniwiki(self.wiki_url)
        wiki.do_import(self.target)
