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
    '-p',
    '--just-parse',
    dest='just_parse',
    help='Parse & show AST nodes',
    action='store_true'
)

#parser.add_argument(
#    '-v',
#    '--verbose',
#    dest='verbose',
#    help='Enable verbose output',
#    action='store_true'
#)
#
#parser.add_argument(
#    '-d',
#    '--debug',
#    dest='debug',
#    help='Enable debug (enable verbose too)',
#    action='store_true'
#)

parser.add_argument(
    '-f',
    '--force',
    dest='force',
    help='Transpile files even if errors',
    action='store_true'
)

parser.add_argument(
    '-n',
    '--no-c',
    dest='no_c',
    help='Do not write C code to file.c',
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

from Kooc.chief import ChiefKooc, KLoadingError

chief = ChiefKooc(just_parse = args.just_parse, write_c = not args.no_c)

# TODO: setup logging
#if args.verbose:
#    chief.verbose = True
#if args.debug:
#    chief.debug = True

try:
    chief.load_files(args.filenames)
except KLoadingError as kle:
    print("There were errors while loading files")
    print('# --  --  --  --  --  --  --  --  --')
    for err in kle.errors:
        print(err)
    print('# --  --  --  --  --  --  --  --  --')
    if not args.force:
        if chief.nb_valid_files():
            print()
            print('Use --force (-f) to process the {} good files'.format(chief.nb_valid_files()))
            print()
        sys.exit(42)

if chief.nb_valid_files() == 0:
    print('No file to process')
    sys.exit()

print('# ' + str(chief.nb_valid_files()) + " files to process")

chief.run()

