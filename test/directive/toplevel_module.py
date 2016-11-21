#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from cnorm import nodes
from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

class DirectiveModule(DirectiveTestCase):

    def test_module(self):
        """Detect module & block"""

        source = """
            @module Test
            {
                int var;
            }
        """

        ast = self.parse(source)
        self.assertTrue("Test" in ast.ktypes)
        self.assertIsInstance(ast.ktypes["Test"](), knodes.KcModule)

        module = ast.ktypes["Test"]()
        self.assertEqual(module.name, "Test")

        in_module_decl = module.body[0]
        self.assertIsInstance(in_module_decl, nodes.Decl)
        self.assertEqual(in_module_decl._name, "var")

if __name__ == '__main__':
    unittest.main()
