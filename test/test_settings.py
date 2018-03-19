# -*- coding: utf-8 -*-

import unittest


class TestSettings(unittest.TestCase):
    def test_config(self):
        from boostnote.settings import config

        self.assertEqual(config.get_config_name()[-13:], 'boostnote.ini')
        self.assertEqual(config.logger, 'dd')
