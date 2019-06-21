# -*- coding: utf-8 -*-
import shutil
from tempfile import mkdtemp
from boostnote.base import Boostnote
from boostnote.storage import Storage
from boostnote.note import Note

import unittest


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.path = mkdtemp()
        self.boost: Boostnote = None

    def tearDown(self) -> None:
        shutil.rmtree(self.path)

    def test_save_notes(self):
        self.boost = Boostnote(self.path)
        storage = self.boost.storages['Default0']

        storage.notes['fdsafsda'] = Note()

        self.boost.save_notes()
