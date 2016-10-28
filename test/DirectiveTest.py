#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, '../src/directive')

from cnorm import nodes
import directive

def count_of_type(target_type, arr):
    count = 0
    for _, decl in enumerate(arr):
        if isinstance(decl, target_type):
            count += 1
    return count

class DirectiveTest(unittest.TestCase):
    """Allow to check if the Directive is conform to the documentation"""

    declparser = directive.Directive()

    def test_import(self):
        """Detect import statement"""

        source = """
            @import "myheader.kh"
        """

        ast = self.declparser.parse(source)
        nb_import = count_of_type(directive.KcImport, ast.body)
        self.assertEqual(nb_import, 1)

        single_import = ast.body[0]
        self.assertEqual(single_import.filepath, "myheader.kh")

    def test_multiple_import(self):
        """Detect multiple import statement"""

        source = """
            @import "myheader.kh"
            @import "otherheader.kh"
        """

        ast = self.declparser.parse(source)
        nb_import = count_of_type(directive.KcImport, ast.body)
        self.assertEqual(nb_import, 2)
        imports = ast.body
        self.assertEqual(imports[0].filepath, "myheader.kh")
        self.assertEqual(imports[1].filepath, "otherheader.kh")

    def test_module(self):
        """Detect module & block"""

        source = """
            @module Test
            {
                int var;
            }
        """

        ast = self.declparser.parse(source)
        nb_import = count_of_type(directive.KcModule, ast.body)
        self.assertEqual(nb_import, 1)

        module = ast.body[0]
        self.assertEqual(module._name, "Test")

        self.assertIsInstance(module.body, directive.KcDeclBlock)

        in_module_decl = module.body.body[0]
        self.assertIsInstance(in_module_decl, nodes.Decl)
        self.assertEqual(in_module_decl._name, "var")

unittest.main()
