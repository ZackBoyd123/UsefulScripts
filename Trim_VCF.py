#!/usr/bin/python3
import sys
import csv
import argparse

parser = argparse.ArgumentParser(description="A script which trims the start and end of a VCF file.")
parser.add_argument("--input", help="Input converted VCF file", required=True)
parser.add_argument("--start",help="Remove all the positions before this value", required=True)
parser.add_argument("--end", help="Remove all positions after this value", required=True)
parser.add_argument("--output", help="Output file name", required=True)
args = parser.parse_args()
pos_start = int(args.start)
pos_end = int(args.end)
file_in = args.input
file_out = args.output

sys.stdout = open(file_out, "w")
with open(file_in) as file:
    data = csv.reader(file, delimiter = "\t")
    next(data, None)
    for line in data:
        if int(pos_start) < int(line[1]) < int(pos_end):
            print("\t".join(line))
