import os
import unittest

import pytest
from pydantic import ValidationError
from src.flowlog_parser import generate_tags, parse_flow_log, parse_lookup_file


class TestParseLookup(unittest.TestCase):
    def test_sample_lookup(self):
        lookup_file_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "lookup_data.txt")
        lookup_dict = parse_lookup_file(lookup_file_path)
        assert len(list(lookup_dict.keys())) > 0
        assert lookup_dict['25,tcp'] == 'sv_P1'

    def test_empty_lookup(self):
        lookup_file_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "empty_lookup.txt")
        lookup_dict = parse_lookup_file(lookup_file_path)
        assert len(list(lookup_dict.keys())) == 0

    def test_bad_lookup(self):
        lookup_file_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "bad_lookup_data.txt")
        with pytest.raises(AttributeError):
            lookup_dict = parse_lookup_file(lookup_file_path)

    def test_sample_flowlog(self):
        flowlog_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "flow_log.txt")
        flow_records = list(parse_flow_log(flowlog_path))
        assert len(flow_records) == 14

    def test_bad_flowlog(self):
        flowlog_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "bad_flowlog.txt")
        with pytest.raises(ValidationError):
            flow_records = list(parse_flow_log(flowlog_path))

    def test_non_existent_flowlog(self):
        flowlog_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "flowlog_non_existent.txt")
        with pytest.raises(FileNotFoundError):
            flow_records = list(parse_flow_log(flowlog_path))

    def test_non_existent_flowlog(self):
        flowlog_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "flowlog_non_existent.txt")
        with pytest.raises(FileNotFoundError):
            flow_records = list(parse_flow_log(flowlog_path))

    def test_generate_tags(self):
        flowlog_path = os.path.join(os.path.dirname(__file__),
                                    "../data",
                                    "flow_log.txt")
        lookup_file_path = os.path.join(os.path.dirname(__file__),
                                        "../data",
                                        "lookup_data.txt")
        tag_counts, port_protocol_counts = generate_tags(lookup_file_path=lookup_file_path,
                                                         flowlog_file_path=flowlog_path)
        assert len(tag_counts.keys()) == 4
        assert tag_counts['Untagged'] == 8