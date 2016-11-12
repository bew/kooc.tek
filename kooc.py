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

parser.add_argument(
    '-v',
    '--verbose',
    dest='verbose',
    help='Enable verbose output',
    action='store_true'
)

parser.add_argument(
    '-d',
    '--debug',
    dest='debug',
    help='Enable debug (enable verbose too)',
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
for f in args.filenames:
    if f == '-':
        f = '/dev/stdin'
    if not os.path.exists(f):
        print('Unkown file: ' + f)
        continue
    if not os.access(f, os.R_OK):
        print('Cannot read file: ' + f)
        continue
    files_to_process.append(f)

if len(files_to_process) == 0:
    print('No file to process')
    sys.exit()


print('loading modules...', end='')
sys.stdout.flush()

from Kooc.directive import directive
print(' done')

for filename_in in files_to_process:
    f = open(filename_in, 'r')
    print('Reading file ' + filename_in)
    content = f.read()
    print('======= Content ======')
    if content[-1:] == '\n':
        content = content[:-1]
    print(content)
    print('=== End of Content ===')

