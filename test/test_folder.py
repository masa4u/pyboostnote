# -*- coding: utf-8 -*-
import os

from boostnote.folder import Folder

import unittest


class TestFolder(unittest.TestCase):

    def test_repr(self):
        folder = Folder('Default', 'Default', 'red')
        self.assertEqual('<Folder: Default, key=Default, note=0>', repr(folder))
        self.assertEqual(folder.color, 'red')
        self.assertEqual(folder.path, '')
