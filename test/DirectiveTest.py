#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys, os

from cnorm import nodes

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../src/directive')

import directive

class DirectiveTest(unittest.TestCase):
    """Allow to check if the Directive is conform to the documentation"""

    koocparser = directive.Directive()

    def test_import(self):
        """Detect import statement"""

        source = """
            @import "myheader.kh"
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.imports, list)
        self.assertEqual(ast.imports[0], "myheader.kh")

    def test_multiple_import(self):
        """Detect multiple import statement"""

        source = """
            @import "myheader.kh"
            @import "myheader.kh"
            @import "otherheader.kh"
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.imports, list)
        self.assertListEqual(ast.imports, ["myheader.kh", "otherheader.kh"])

    def test_import_kc(self):
        """Do not import kooc source file"""

        source = """
            @import "source.kc"
        """

        #TODO: use custom exception
        with self.assertRaises(Exception):
            self.koocparser.parse(source)

    def test_module(self):
        """Detect module & block"""

        source = """
            @module Test
            {
                int var;
            }
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.body[0], directive.KcModule)

        module = ast.body[0]
        self.assertEqual(module._name, "Test")

        in_module_decl = module.body[0]
        self.assertIsInstance(in_module_decl, nodes.Decl)
        self.assertEqual(in_module_decl._name, "var")

    #TODO: tests on top_level, class, inheritance_list, virtuals, members, typenames, ........

unittest.main()
