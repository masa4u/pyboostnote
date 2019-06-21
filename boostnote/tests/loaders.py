# -*- coding: utf-8 -*-
import unittest


def boostnote_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite
