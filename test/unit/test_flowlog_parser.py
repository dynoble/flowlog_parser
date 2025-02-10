import os
import unittest
from src.flowlog_parser import parse_lookup_file


class TestParseLookup(unittest.TestCase):
    def test_sample(self):
        lookup_file_path = os.path.join(os.path.dirname(__file__), "../data", "lookup_data.txt")
        lookup_dict = parse_lookup_file(lookup_file_path)
