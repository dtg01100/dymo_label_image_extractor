#!/usr/bin/env python3

import argparse
import backend
import os

parser = argparse.ArgumentParser()
parser.add_argument("input_path", help="Input .label file path", nargs='+')
parser.add_argument("-o", "--output_directory", help="Output directory path")
arguments = parser.parse_args()

extractor = backend.ImageExtractor()

extractor.output_path = arguments.output_directory

if extractor.output_path is None:
    extractor.write_stdout = True
for entry in arguments.input_path:
    extractor.input_path = entry
    if os.path.isdir(entry):
        extractor.is_batch = True
    else:
        extractor.is_batch = False
    if extractor.check_for_ready():
        extractor.start_extracting()
