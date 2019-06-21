# -*- coding: utf-8 -*-

import unittest

from boostnote.note import Note


class TestNote(unittest.TestCase):
    def setUp(self):
        pass

    def test_note_creation(self):
        note = Note()
        self.assertEqual(note.title, '')

        self.assertTrue(repr(note).startswith('<Note:'))
