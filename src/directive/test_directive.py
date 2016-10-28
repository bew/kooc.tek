#!/usr/bin/env python
# -*- coding: utf-8 -*-


from directive import Directive
import sys

p = Directive()
res = p.parse_file(sys.argv[1])

print(res.to_yml())

#import unittest
