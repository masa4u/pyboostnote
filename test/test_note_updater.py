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
        fp.extractall(path)


class TestNoteUpdater(unittest.TestCase):
    def setUp(self):
        self.source_path = mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.source_path)

    def test_note_updater(self):
        bnote = Boostnote([self.source_path])
        updater = NoteUpdater(bnote, True)

        # Headings
        updater.add_replace('([#]+ )(.*?)([ ]+[#]+)\n', '\\1\\2\n')
        updater.add_replace('(= )(.*?)([ ]+=)\n', '# \\2\n')
        updater.add_replace('([=]{2} )(.*?)([ ]+[=]{2})\n', '## \\2\n')
        updater.add_replace('([=]{3} )(.*?)([ ]+[=]{3})\n', '### \\2\n')
        updater.add_replace('([=]{4} )(.*?)([ ]+[=]{4})\n', '#### \\2\n')
        # special func
        updater.add_replace('\[\[TableOfContents\]\]', '[TOC]')
        # Emphasis
        updater.add_replace("([']{3})(.*?)([']{3})", "**\\2**")
        updater.add_replace("([']{2})(.*?)([']{2})", "*\\2*")
        # code
        special = ''.join(['\\' + x for x in '+-*/= .,;:!?#&$%@|^(){}[]~<>\''])
        inner_code = '[ ]*[\{]{3}([#!a-z ]*)\n([\w\s가-힣' + special + ']*)[\}]{3}'
        updater.add_replace(inner_code, '```\\1```\n')
        # Link
        updater.add_replace(
            '(\[)(http[s]?://[\w\-./%#가-힣]+) ([a-zA-Z0-9.가-힣 \+\/]+)(\])',
            '[\\3](\\2)')

        updater.do_rename_file()
        updater.find_inner_link()
        updater.do_update()
