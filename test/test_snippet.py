# -*- coding: utf-8 -*-
import os

from boostnote.snippets import Snippet, Snippets

import unittest


class TestSnippet(unittest.TestCase):

    def test_snippet(self):
        s = Snippet()

        s['name'] = 'dfdafs'
        s['mode'] = 'fdsafdsa'

        s['content'] = 'fdsafdsa'

        ss = Snippets()

        self.assertTrue(s.name, s['name'])
        self.assertTrue(s.mode, s['mode'])
        self.assertTrue(s.content, s['content'])
        
