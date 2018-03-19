# -*- coding: utf-8 -*-

import unittest

from boostnote.note import Note


class TestNote(unittest.TestCase):
    def setUp(self):
        pass

    def test_note_creation(self):
        note = Note()
        self.assertEquals(note.title, '')


if __name__ == '__main__':
    unittest.main()
