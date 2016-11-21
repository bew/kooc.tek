#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from cnorm import nodes
from Kooc import knodes
from Kooc.directive.typedliteral import TypedLiteral

class TypedLiteralTest(unittest.TestCase):
    """Test the TypedLiteral parser"""

    tl_parser = TypedLiteral()

    def test_int(self):
        """C int"""

        ast = self.tl_parser.parse('43')
        self.assertIsInstance(ast, knodes.KcTypedLiteral)
        self.assertEqual(ast.value, '43')
        self.assertIsInstance(ast.expr_type, nodes.PrimaryType)
        self.assertEqual(ast.expr_type._identifier, 'int')

    def test_double(self):
        """C double"""

        ast = self.tl_parser.parse('4.3')
        self.assertIsInstance(ast, knodes.KcTypedLiteral)
        self.assertEqual(ast.value, '4.3')
        self.assertIsInstance(ast.expr_type, nodes.PrimaryType)
        self.assertEqual(ast.expr_type._identifier, 'double')

    def test_char(self):
        """C char"""

        ast = self.tl_parser.parse("'0'")
        self.assertIsInstance(ast, knodes.KcTypedLiteral)
        self.assertEqual(ast.value, "'0'")
        self.assertIsInstance(ast.expr_type, nodes.PrimaryType)
        self.assertEqual(ast.expr_type._identifier, 'char')

    def test_string(self):
        """C string (char*)"""

        ast = self.tl_parser.parse('"Hello world !"')
        self.assertIsInstance(ast, knodes.KcTypedLiteral)
        self.assertEqual(ast.value, '"Hello world !"')
        self.assertIsInstance(ast.expr_type, nodes.PrimaryType)
        self.assertEqual(ast.expr_type._identifier, 'char')
        self.assertIsInstance(ast.expr_type._decltype, nodes.PointerType)

if __name__ == '__main__':
    unittest.main()
