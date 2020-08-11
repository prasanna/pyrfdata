import os
import sys
import shutil
import inspect
import unittest
import errno
import csv
import yaml
from unittest.mock import MagicMock

src_dir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../src/pyrfdata")))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from partition import partition


class TestPartition(unittest.TestCase):
    def test_partitions_when_partitions_fit_perfectly(self):
        partition_size = 10
        rows = 100
        partitions = partition(rows, partition_size)
        self.assertEqual(10, len(partitions))
        expected_partitions = [{'start': 0, 'end': 9}, {'start': 10, 'end': 19}, {'start': 20, 'end': 29}, {'start': 30, 'end': 39}, {'start': 40, 'end': 49}, {'start': 50, 'end': 59}, {'start': 60, 'end': 69}, {'start': 70, 'end': 79}, {'start': 80, 'end': 89}, {'start': 90, 'end': 99}]
        self.assertEqual(expected_partitions, partitions)

    def test_partitions_when_partitions_dont_fit_perfectly(self):
        partition_size = 10
        rows = 95
        partitions = partition(rows, partition_size)
        self.assertEqual(10, len(partitions))
        expected_partitions = [{'start': 0, 'end': 9}, {'start': 10, 'end': 19}, {'start': 20, 'end': 29}, {'start': 30, 'end': 39}, {'start': 40, 'end': 49}, {'start': 50, 'end': 59}, {'start': 60, 'end': 69}, {'start': 70, 'end': 79}, {'start': 80, 'end': 89}, {'start': 90, 'end': 94}]
        self.assertEqual(expected_partitions, partitions)