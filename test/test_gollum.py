# -*- coding: utf-8 -*-
import os
import shutil
import unittest
from tempfile import mkdtemp

from boostnote.importer.gollum import MarkdownGollum


class TestGollum(unittest.TestCase):
    def setUp(self):
        self.gollum_path = mkdtemp()
        self.target = mkdtemp()

        with open(os.path.join(self.gollum_path, 'test.md'), 'w') as fp:
            fp.write('## test\nmigration!!')

    def tearDown(self) -> None:
        shutil.rmtree(self.gollum_path)
        shutil.rmtree(self.target)

    def test_migration(self):
        md_storage = MarkdownGollum(self.gollum_path)
        md_storage.do_import(self.target)
