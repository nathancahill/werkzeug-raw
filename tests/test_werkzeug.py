
import os
import unittest
import werkzeug_raw


VALID_DIR = os.path.join('tests', 'raw', 'valid')
INVALID_DIR = os.path.join('tests', 'raw', 'invalid')


class WerkzeugTest(unittest.TestCase):
    def test_valid(self):
        for fn in os.listdir(VALID_DIR):
            with open(os.path.join(VALID_DIR, fn)) as f:
                werkzeug_raw.environ(f.read())

    def test_invalid(self):
        for fn in os.listdir(INVALID_DIR):
            with open(os.path.join(INVALID_DIR, fn)) as f:
                with self.assertRaises(werkzeug_raw.BadRequestSyntax):
                    werkzeug_raw.environ(f.read())
