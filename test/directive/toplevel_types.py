#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

class DirectiveTypes(DirectiveTestCase):

    def test_types_no_class(self):
        """ktype but no C type for a module"""

        source = """
            @module Bla {}
        """

        ast = self.parse(source)
        self.assertEqual(len(ast.types), 0)
        self.assertEqual(len(ast.ktypes), 1)

    def test_types_for_class(self):
        """A class add a new typename"""

        source = """
            @class C {}
        """

        ast = self.parse(source)
        self.assertTrue('C' in ast.ktypes)
        self.assertTrue('C' in ast.types)

    def test_types_for_multi_classes(self):
        """types for class parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        ast = self.parse(source)
        self.assertTrue('A' in ast.ktypes)
        self.assertTrue('B' in ast.ktypes)
        self.assertTrue('C' in ast.ktypes)
        self.assertTrue('A' in ast.types)
        self.assertTrue('B' in ast.types)
        self.assertTrue('C' in ast.types)

if __name__ == '__main__':
    unittest.main()
