#!/usr/bin/env python
# -*- coding: utf-8 -*-


from directive import Directive
import sys

p = Directive()
ast = p.parse_file(sys.argv[1])

print(ast.to_yml())

if hasattr(ast, "imports"):
    print("> imports:", ast.imports)
if hasattr(ast, "typenames"):
    print("> typenames:", ast.typenames)

#import unittest
