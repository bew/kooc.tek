#!/usr/bin/env python3

# vim:set et sw=4 ts=4 ft=python:

import sys
import os
from argparse import ArgumentParser

parser = ArgumentParser(
    prog='kooc',
    description='Kind Of Objective C - by paccar_c\'s team'
)

parser.add_argument(
    '-y',
    '--yml',
    dest='yml',
    help='Show AST nodes as yml',
    action='store_true'
)

#TODO: enable verbose logging
parser.add_argument(
    '-v',
    '--verbose',
    dest='verbose',
    help='Enable verbose output',
    action='store_true'
)

#TODO: enable debug logging
parser.add_argument(
    '-d',
    '--debug',
    dest='debug',
    help='Enable debug (enable verbose too)',
    action='store_true'
)

parser.add_argument(
    '-f',
    '--fail-file-error',
    dest='fail_on_file_error',
    help='Do not start if any file error',
    action='store_true'
)

parser.add_argument(
    'filenames',
    help='process KFILE with kooc',
    metavar='KFILE',
    type=str,
    nargs='*'
)

args = parser.parse_args()

files_to_process = []
for fpath in args.filenames:
    if fpath == '-':
        fpath = '/dev/stdin'
    if not os.path.exists(fpath):
        print('Unkown file: ' + fpath)
        continue
    if not os.path.isfile(fpath):
        print('Not a regular file: ' + fpath)
        continue
    if not os.access(fpath, os.R_OK):
        print('Cannot read file: ' + fpath)
        continue
    files_to_process.append(fpath)

if len(files_to_process) == 0:
    print('No file to process')
    sys.exit()

if len(args.filenames) != len(files_to_process) and args.fail_on_file_error:
    print("File error detected, exiting")
    sys.exit(42)

print('# ' + str(len(files_to_process)) + " files to process")

print('loading modules...', end='')
sys.stdout.flush()

from Kooc import directive
print(' done')

for filename_in in files_to_process:
    f_in = open(filename_in, 'r')
    print()
    print('Reading file ' + filename_in)
    content = f_in.read()
    print('======= Content ======')
    if content[-1:] == '\n':
        content = content[:-1]
    print(content)
    print('=== End of Content ===')

