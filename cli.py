#!/usr/bin/env python3

import argparse
import backend

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Input .label file path")
parser.add_argument("-o", "--output_directory", help="Output directory path")
parser.add_argument("-s", "--stdout", help="Write extracted images to stdout", action='store_true')
arguments = parser.parse_args()

extractor = backend.ImageExtractor()
extractor.is_batch = False

print(arguments.input_file)
print(arguments.output_directory)
print(arguments.stdout)

extractor.input_path = arguments.input_file
extractor.output_path = arguments.output_directory
extractor.write_stdout = arguments.stdout
if extractor.check_for_ready():
    extractor.start_extracting()
