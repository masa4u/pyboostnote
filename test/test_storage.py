# -*- coding: utf-8 -*-
import os
from boostnote.storage import Storage

import unittest


class TestStorage(unittest.TestCase):

    def test_init_test(self):
        self.assertRaises(FileNotFoundError, Storage, **{'path': ''})

    def test_repr(self):
        s = Storage(os.path.dirname(__file__))
        self.assertTrue(repr(s).startswith('<Storage:'))