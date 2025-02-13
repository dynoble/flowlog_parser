# This module parses flow logs and tags them
# More about flow log : https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html

# execution
python3.10 src/flowlog_parser.py -lookup test/data/lookup_data.txt -flowlog test/data/flow_log.txt -output test/data_out/output.txt

# install requirements
python3.10 -m pip install -r requirements.txt

# run tests
python3.10 -m pytest test

# test cases
- version 2 flow log
- invalid flow log
- invalid lookup table
- empty flow log
- empty lookup table
- non-existent input file locations