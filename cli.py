#!/usr/bin/env python3

import argparse
import backend
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Input .label file path")
parser.add_argument("-o", "--output_directory", help="Output directory path")
arguments = parser.parse_args()

extractor = backend.ImageExtractor()
extractor.is_batch = False

extractor.input_path = arguments.input_file
try:
    extractor.output_path = arguments.output_directory
except TypeError:
    extractor.write_stdout = True
if extractor.check_for_ready():
    extractor.start_extracting()
else:
    sys.stderr.write("Incorrect command line arguments")
