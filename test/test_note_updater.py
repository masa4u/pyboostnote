# -*- coding: utf-8 -*-
import os
import shutil
import tarfile
import unittest
from tempfile import mkdtemp

from boostnote.base import Boostnote
from boostnote.note_updater import NoteUpdater


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


class TestNoteUpdater(unittest.TestCase):
    def setUp(self):
        self.source_path = mkdtemp()
        extract_file(self.source_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.source_path)

    def test_note_updater(self):
        bnote = Boostnote([self.source_path])
        updater = NoteUpdater(bnote, True)

        updater.add_replace(r'\(:storage[\\|/]([a-z0-9\-]+)[\\|/]([\w\.]+)\)', '\\1\\2\n')

        updater.do_rename_file()
        updater.find_inner_link()
        updater.do_update()

        updater.check()


if __name__ == '__main__':
    unittest.main()
