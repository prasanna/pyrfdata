import os
import sys
import inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../src")))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from pyrfdata import request


class TestRequest(unittest.TestCase):
    def test_request_knows_that_data_generation_was_not_requested_when_only_arg_p_is_passed(self):
        r = request.Request(["p"])
        self.assertFalse(r.data_generation_requested())

    def test_request_knows_that_data_generation_was_requested_when_arg_g_is_passed(self):
        r = request.Request(["g"])
        self.assertTrue(r.data_generation_requested())

    def test_request_knows_that_data_generation_was_requested_when_arg_gen_is_passed(self):
        r = request.Request(["gen"])
        self.assertTrue(r.data_generation_requested())

    def test_request_knows_that_data_generation_was_requested_when_arg_generate_is_passed(self):
        r = request.Request(["generate"])
        self.assertTrue(r.data_generation_requested())

    def test_request_knows_that_data_generation_was_requested_when_no_args_are_passed(self):
        r = request.Request([""])
        self.assertTrue(r.data_generation_requested())

    def test_request_knows_that_data_processing_was_not_requested_when_only_arg_g_is_passed(self):
        r = request.Request(["g"])
        self.assertFalse(r.data_processing_requested())

    def test_request_knows_that_data_processing_was_requested_when_arg_p_is_passed(self):
        r = request.Request(["p"])
        self.assertTrue(r.data_processing_requested())

    def test_request_knows_that_data_processing_was_requested_when_arg_proc_is_passed(self):
        r = request.Request(["proc"])
        self.assertTrue(r.data_processing_requested())

    def test_request_knows_that_data_processing_was_requested_when_arg_process_is_passed(self):
        r = request.Request(["process"])
        self.assertTrue(r.data_processing_requested())

    def test_request_knows_that_data_processing_was_requested_when_no_args_are_passed(self):
        r = request.Request([""])
        self.assertTrue(r.data_processing_requested())

    def test_request_knows_that_both_data_generation_and_processing_was_requested_when_both_p_and_g_args_are_passed(self):
        r = request.Request("p g".split(" "))
        self.assertTrue(r.data_generation_requested())
        self.assertTrue(r.data_processing_requested())

    def test_request_defaults_parallel_processes_to_1_when_generating(self):
        r = request.Request(["g"])
        self.assertEqual(1, r.parallel_processes)

    def test_request_defaults_partition_size_to_1000_when_generating(self):
        r = request.Request(["g"])
        self.assertEqual(1000, r.partition_size)

    def test_request_sets_parallel_processes_to_10_when_generating_with_l_param(self):
        r = request.Request("g l:10".split(" "))
        self.assertEqual(10, r.parallel_processes)

    def test_request_sets_partition_size_to_10_when_generating_with_s_param(self):
        r = request.Request("g s:10".split(" "))
        self.assertEqual(10, r.partition_size)

    def test_request_sets_template_when_generating_with_template_param(self):
        r = request.Request("g t:/tmp/t.yml".split(" "))
        self.assertEqual("/tmp/t.yml", r.template.location())

    def test_request_defaults_template_to_template_yml_when_generating_without_template_param(self):
        r = request.Request(["g"])
        self.assertEqual("template.yml", r.template.location())
