import os
import sys
import inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../src")))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


class TestPyrfData(unittest.TestCase):
    def test_pyrfdata(self):
        self.assertEqual(0, 0)
