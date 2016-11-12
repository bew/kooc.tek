#!/usr/bin/python3
# -*- coding: utf-8 -*-                                                                                                                                                                      
import mangling
import sys

if not (len(sys.argv) is 2):
    print('./test.py "filename"')
    exit(1)

from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c

cparse = Declaration()
ast = cparse.parse_file(sys.argv[1])
for index, decl in enumerate(ast.body):
    cString = decl.to_c();
    print(cString, end='')
    print(decl)
    mangled = ""
    try:
        mangled = mangling.mangle(decl, mangling.OriginIsModule, 'DUMMY_MODUL_NAME')._name
        print(mangled)
        unmangled = mangling.unmangle(mangled)
        print(unmangled)
        print(unmangled.decl.to_c())
    except Exception as e:
        print(str(e))
    if index < len(ast.body) - 1:
        print('')
