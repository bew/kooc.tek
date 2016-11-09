#!/usr/bin/env python
# -*- coding: utf-8 -*-

from directive import Directive
import sys

p = Directive()
ast = p.parse_file(sys.argv[1])

print(ast.to_yml())

print("> imports:", ast.kimports)
print("> typenames:", ast.ktypenames)
