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

from template import Template
from request import Request


class TestTemplate(unittest.TestCase):
    def test_raises_exception_if_template_is_not_found(self):
        t = Template("i_dont_exist", Request())
        self.assertRaises(FileNotFoundError, t.load)

    def test_template_generates_what_it_is_supposed_to(self):
        t = Template(self.template_location, Request())
        t.load()
        self.assertEqual("tmp/data.csv", t.files[0].location)

        t.generate()
        self.assertTrue(os.path.isfile(t.files[0].location))

        with open(t.files[0].location, "r") as f:
            rows = 0
            data_reader = csv.reader(f, delimiter=',')
            for i, row in enumerate(data_reader):
                rows += 1
                if i == 0:
                    self.assertEqual("id", row[0])
                    self.assertEqual("name", row[1])
                    self.assertEqual("value000", row[2])
                    self.assertEqual("value001", row[3])
                elif i == 1:
                    self.assertEqual("ABC-0001", row[0])
                    self.assertRegex(row[1], "\w\w\w\w\w")
                    try:
                        float(row[2])
                    except ValueError:
                        self.fail("String " + row[2] + " is not a float.")
                elif i == 2:
                    self.assertEqual("ABC-0002", row[0])
            self.assertEqual(3, rows)

    def setUp(self):
        self.tmp_dir = "tmp"
        self.template_dir = self.tmp_dir
        self.template_file_name = "template.yml"
        self.template_location = self.template_dir + "/" + self.template_file_name
        self.ensure_tmp_dir_does_not_exist()
        self.create_template_yml()

    def create_template_yml(self, spec={}, rows=1):
        self.create_template_dir_if_it_doesnt_exist()
        template_spec = """
  files:
    - name: tmp/data.csv
      rows: 2
      cols:
        - name: id
          type: string
          generator:
            name: integer_sequence
            params:
              min: 1
              max: 9999
              prefix: "ABC-"
              padding:
                length: 4
                zero_or_space: zero
        - name: name
          type: string
          generator:
            name: random_string
            params:
                length: 5
        - name:
            type: string
            generator:
              name: integer_sequence
              params:
                min: 0
                max: 999
                prefix: "value"
                padding:
                  zero_or_space: zero
                  length: 3
          repeat: 2
          type: float
          generator:
            name: random_float
            params:
              min: 0
              max: 100

"""
        # template_yml = yaml.dump(yaml.load(template_spec, Loader=yaml.FullLoader))

        out = open(self.template_location, "w", encoding="utf-8")
        out.write(template_spec)
        out.close()

    def create_template_dir_if_it_doesnt_exist(self):
        try:
            os.makedirs(self.template_dir, 0o755)
        except OSError as err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(self.template_dir):
                raise

    def tearDown(self) -> None:
        self.ensure_tmp_dir_does_not_exist()

    def ensure_tmp_dir_does_not_exist(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

