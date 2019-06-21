# -*- coding: utf-8 -*-

import unittest
from boostnote.importer.converter import BaseConveter
class TestBaseConveter(unittest.TestCase):

    def test_init(self):
        b = BaseConveter('')

        self.assertRaises(NotImplementedError, b.converter, **{'note': ''})
