# coding : utf-8
from flask_script import Command
import unittest

class TestAll(Command):

    def run(self):
        self.test_all()

    def test_all(self):
        tests = unittest.TestLoader().discover('.')
        unittest.TextTestRunner(verbosity=1).run(tests)