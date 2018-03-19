# -*- coding: utf-8 -*-
import os
import unittest

from boostnote.migration.gollum import MarkdownGollum
from tempfile import TemporaryDirectory


class TestGollum(unittest.TestCase):
    def setUp(self):
        self.gollum_path = TemporaryDirectory()
        self.target = TemporaryDirectory()

        with open(os.path.join(self.gollum_path.name, 'test.md'), 'w') as fp:
            fp.write('## test\nmigration!!')

    def test_migration(self):
        md_storage = MarkdownGollum(self.gollum_path.name)
        md_storage.do_import(self.target.name)
