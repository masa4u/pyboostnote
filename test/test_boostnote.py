# -*- coding: utf-8 -*-
import os
import shutil
import tarfile
import unittest
from tempfile import mkdtemp

from boostnote import Boostnote


def extract_file(path):
    filename = os.path.join(os.path.dirname(__file__), 'sample', 'boostnote.tar.gz')

    with tarfile.open(filename, 'r:gz') as fp:
        fp.extractall(path)


class TestBoostnote(unittest.TestCase):
    def setUp(self):
        self.temp_path = mkdtemp()
        extract_file(self.temp_path)
        self.boostnote = Boostnote([self.temp_path])

    def tearDown(self):
        shutil.rmtree(self.temp_path)

    def test_find(self):
        notes = []
        for storage, folder, note in self.boostnote.find_note(lambda x: x.title != 'ubuntu'):
            notes.append(note)
        self.assertEqual(len(notes), 4, "check note size")

    def test_walk_note(self):
        notes = []
        for storage, folder, note in self.boostnote.walk_note():
            notes.append(note)
        self.assertEqual(len(notes), 4, "check note size")

    def test_repr(self):
        self.assertEqual(str(self.boostnote).split(' ')[0], '<Boostnote')


if __name__ == '__main__':
    unittest.main()
