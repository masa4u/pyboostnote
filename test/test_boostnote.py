# -*- coding: utf-8 -*-

import unittest
from boostnote.settings import config
from boostnote import Boostnote


class TestBoostnote(unittest.TestCase):
    def setUp(self):
        self.boostnote = Boostnote(config.path)

    def test_find(self):
        for storage, folder, note in self.boostnote.find_note(lambda x: x.title == 'ubuntu'):
            pass

    def test_walk_note(self):
        for storage, folder, note in self.boostnote.walk_note():
            pass

    def test_repr(self):
        self.assertEqual(str(self.boostnote).split(' ')[0], '<Boostnote')
