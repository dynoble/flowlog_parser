

import argparse
from collections import Counter
from pathlib import Path
from csv import DictReader
import socket

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


import data_model
import utils

def generate_port_protocol_mapping():
    prefix = "IPPROTO_"
    mapping = {num: protocol_name[len(prefix):].lower()
               for protocol_name, num in vars(socket).items()
               if protocol_name.startswith(prefix)}
    return  mapping


def parse_lookup_file(lookup_file: str):
    lookup_file_path = Path(lookup_file)
    utils.validate_file_path(lookup_file_path)
    lookup_dict = {}
    with lookup_file_path.open() as f:
        reader = DictReader(f, delimiter=',')
        for row in reader:
            formatted_row = {k.strip(): v.strip() for k,v in row.items()}
            dst_port = formatted_row['dstport'].strip()
            protocol = formatted_row['protocol'].strip().lower()
            tag = formatted_row['tag'].strip()
            lookup_dict[f'{dst_port},{protocol}'] = tag
    return lookup_dict


def parse_flow_log(flowlog_file: str):
    flowlog_file_path = Path(flowlog_file)
    utils.validate_file_path(flowlog_file_path)
    custom_header = list(data_model.FlowLogRecord.model_fields.keys())
    with flowlog_file_path.open() as f:
        reader = DictReader(f, delimiter=' ', fieldnames=custom_header)
        for row in reader:
            record = data_model.FlowLogRecord.model_validate(row)
            yield record


def generate_tags(lookup_file_path, flowlog_file_path):
    port_protocol_mapping = generate_port_protocol_mapping()
    lookup_dict = parse_lookup_file(lookup_file_path)
    tag_counts = Counter()
    port_protocol_counts = Counter()
    for flow_record in parse_flow_log(flowlog_file_path):
        protocol_num_to_name = port_protocol_mapping.get(flow_record.protocol)
        if not protocol_num_to_name:
            raise Exception('Failed to convert protocol number {flow_record.protocol} to name. Lookup failed')
        lookup_key = f'{flow_record.dstport},{protocol_num_to_name}'
        port_protocol_counts[lookup_key] += 1
        if lookup_key in lookup_dict:
            tag_counts[lookup_dict[lookup_key]] += 1
        else:
            tag_counts['Untagged'] += 1
    return tag_counts, port_protocol_counts


def parse_arguments():
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument("-lookup", help="path of lookup file", required=True)
    arg_parser.add_argument("-flowlog", help="path of flow log file", required=True)
    arg_parser.add_argument("-output", help="path where output file should be written", required=True)
    args = arg_parser.parse_args()
    return args


def write_output(output_file_path, tag_counts, port_protocol_counts):
    output_file_path_obj = Path(output_file_path)
    with output_file_path_obj.open("w") as fp:
        fp.write(f"Tag Counts:\nTag,Count\n")
        for tag in sorted(tag_counts.keys(), reverse=True):
            fp.write(f"{tag}, {tag_counts[tag]}\n")
        fp.write(f"Port/Protocol Combination Counts: \nPort,Protocol,Count\n")
        for k in sorted(port_protocol_counts.keys(), key=lambda x: int(x.split(',')[0])):
            fp.write(f'{k}, {port_protocol_counts[k]}\n')




def main():
    args = parse_arguments()
    tag_counts, port_protocol_counts = generate_tags(args.lookup, args.flowlog)
    write_output(args.output, tag_counts, port_protocol_counts)

if __name__ == "__main__":
    main()
