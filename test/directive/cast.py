#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from cnorm import nodes
from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

class DirectiveCast(DirectiveTestCase):

    def test_builtin_type(self):
        """Kooc Cast to one C type"""

        source = """
            @!(int)[MyModule.my_float];
        """

        ast = self.parse_in_block(source)

        expr_stmt = ast.body[0]
        kexpr = expr_stmt.expr
        self.assertIsInstance(kexpr, knodes.KcLookup)

        self.assertIsInstance(kexpr.expr_type, nodes.PrimaryType)
        self.assertEqual(kexpr.expr_type._identifier, 'int')

    def test_assign_to(self):
        """C type assignation to a kooc cast"""

        source = """
            @!(int)[MyModule.my_var] = 42;
        """

        ast = self.parse_in_block(source)

        expr_stmt = ast.body[0]
        bin_expr = expr_stmt.expr

        kexpr = bin_expr.params[0]  # assign to
        value = bin_expr.params[1] # assign what

        self.assertIsInstance(kexpr, knodes.KcLookup)
        self.assertIsInstance(kexpr.expr_type, nodes.PrimaryType)
        self.assertEqual(kexpr.expr_type._identifier, 'int')

    def test_cannot_cast_non_kooc_expr(self):
        """Parsing must fails on Kooc casting a non Kooc expression"""

        source = """
            int a = @!(int)4;
        """

        with self.assertRaises(Exception):
            self.parse(source)

if __name__ == '__main__':
    unittest.main()
