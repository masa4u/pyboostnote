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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(fp, path)


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
        self.assertEqual(len(notes), 3, "check note size")

    def test_walk_note(self):
        notes = []
        for storage, folder, note in self.boostnote.walk_note():
            notes.append(note)
        self.assertEqual(len(notes), 3, "check note size")

    def test_repr(self):
        self.assertEqual(str(self.boostnote).split(' ')[0], '<Boostnote')


if __name__ == '__main__':
    unittest.main()
