#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from cnorm import nodes
from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

class DirectiveCall(DirectiveTestCase):

    def test_static_call(self):

        source = """
            int a = [MyModule some_function];
            int b = [MyClass some_method :&obj :1 :2 :3.3];
        """

        ast = self.parse(source)
        self.assertIsInstance(ast.body[0], nodes.Decl)

        decl1 = ast.body[0]
        self.assertIsInstance(decl1._assign_expr, knodes.KcCall)

        call = decl1._assign_expr
        self.assertEqual(call.context, 'MyModule')
        self.assertEqual(call.function, 'some_function')
        self.assertListEqual(call.params, [])

        decl2 = ast.body[1]
        self.assertIsInstance(decl2._assign_expr, knodes.KcCall)

        call = decl2._assign_expr
        self.assertEqual(call.context, 'MyClass')
        self.assertEqual(call.function, 'some_method')
        self.assertIsInstance(call.params, list)
        self.assertEqual(len(call.params), 4)

if __name__ == '__main__':
    unittest.main()
