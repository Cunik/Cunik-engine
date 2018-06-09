# coding : utf-8
import unittest


def test_all():
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(tests)