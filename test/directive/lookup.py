#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from cnorm import nodes
from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

class DirectiveLookup(DirectiveTestCase):

    def test_simple_in_top_level(self):

        source = """
            int var = [MyModule.some_variable];
        """

        ast = self.parse(source)
        self.asserts_for_simple(ast)

    def test_simple_in_block(self):

        source = """
            int var = [MyModule.some_variable];
        """

        ast = self.parse_in_block(source)
        self.asserts_for_simple(ast)

    # helper
    def asserts_for_simple(self, ast):
        self.assertIsInstance(ast.body[0], nodes.Decl)

        decl = ast.body[0]
        self.assertIsInstance(decl._assign_expr, knodes.KcLookup)

        lookup = decl._assign_expr
        self.assertEqual(lookup.context, 'MyModule')
        self.assertEqual(lookup.member, 'some_variable')

if __name__ == '__main__':
    unittest.main()
