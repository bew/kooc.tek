#!/usr/bin/env python3

# vim:set et sw=4 ts=4 ft=python:

import sys
import os
from argparse import ArgumentParser

parser = ArgumentParser(
    prog='kooc',
    description='Kind Of Objective C - Kooc to C transpiler - by paccar_c\'s team'
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
    '-f',
    '--force',
    dest='force',
    help='Transpile files even if errors',
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

if len(args.filenames) != len(files_to_process) and not args.force:
    print("File error detected, exiting")
    sys.exit(42)

print('# ' + str(len(files_to_process)) + " files to process")

print('loading modules...', end='')
sys.stdout.flush()

from Kooc.chief import ChiefKooc, KLoadingError

print(' done')

chief = ChiefKooc()

# TODO: setup logging
if args.verbose:
    chief.verbose = True
if args.debug:
    chief.debug = True

try:
    chief.load_files(files_to_process)
except KLoadingError as e:
    # TODO: better loading error handling
    print("There were errors while loading files")
    sys.exit(42)

chief.run()

