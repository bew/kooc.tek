#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys, os

from cnorm import nodes

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../src/directive')

import directive
import knodes

class DirectiveTest(unittest.TestCase):
    """Allow to check if the Directive is conform to the documentation"""

    koocparser = directive.Directive()

    def test_import(self):
        """Detect import statement"""

        source = """
            @import "myheader.kh"
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.kimports, list)
        self.assertEqual(ast.kimports[0], "myheader.kh")

    def test_multiple_import(self):
        """Detect multiple import statement"""

        source = """
            @import "myheader.kh"
            @import "myheader.kh"
            @import "otherheader.kh"
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.kimports, list)
        self.assertListEqual(ast.kimports, ["myheader.kh", "otherheader.kh"])

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
        self.assertTrue("Test" in ast.ktypes)
        self.assertIsInstance(ast.ktypes["Test"], directive.KcModule)

        module = ast.ktypes["Test"]
        self.assertEqual(module.name, "Test")

        in_module_decl = module.body[0]
        self.assertIsInstance(in_module_decl, nodes.Decl)
        self.assertEqual(in_module_decl._name, "var")

    def test_top_level(self):
        """@ keywords must be in top level"""

        source = """
            {
                @module Bla
                {
                }
            }
        """

        with self.assertRaises(Exception):
            self.koocparser.parse(source)

    def test_typenames_no_class(self):
        """No typename for a module"""

        source = """
            @module Bla {}
        """

        ast = self.koocparser.parse(source)
        self.assertListEqual(ast.ktypenames, [])

    def test_typenames_for_class(self):
        """A class add a new typename"""

        source = """
            @class C {}
        """

        ast = self.koocparser.parse(source)
        self.assertListEqual(ast.ktypenames, ["C"])

    def test_typenames_for_multi_classes(self):
        """typenames for class parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        ast = self.koocparser.parse(source)
        self.assertListEqual(ast.ktypenames, ["A", "B", "C"])

    def test_class_inheritance(self):
        """A class with parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        ast = self.koocparser.parse(source)
        self.assertTrue("C" in ast.ktypes)
        self.assertIsInstance(ast.ktypes["C"], knodes.KcClass)

        klass = ast.ktypes["C"]
        self.assertTrue("A" in klass.parents)
        self.assertTrue("B" in klass.parents)
        self.assertIsInstance(klass.parents, dict)

        self.assertIsInstance(klass.parents["A"], knodes.KcClass)

    def test_class_inheritance_fail(self):
        """TODO: doc"""

        source = """
            @class C : DFYUI {}
        """

        with self.assertRaises(Exception):
            self.koocparser.parse(source)


    #TODO: tests on virtuals, members, ........

class DirectiveLookup(unittest.TestCase):

    koocparser = directive.Directive()

    def test_simple_in_top_level(self):
        """TODO: doc"""

        source = """
            int var = [MyModule.some_variable];
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.body[0], nodes.Decl)

        decl = ast.body[0]
        self.assertIsInstance(decl._assign_expr, knodes.KcLookup)

        lookup = decl._assign_expr
        self.assertEqual(lookup.context, 'MyModule')
        self.assertEqual(lookup.member, 'some_variable')

    def test_simple_in_block(self):
        """TODO: doc"""

        source = """
            void some_function()
            {
                int var = [MyModule.some_variable];
            }
        """

        ast = self.koocparser.parse(source)
        self.assertIsInstance(ast.body[0], nodes.Decl)

        func = ast.body[0]
        self.assertIsInstance(func._ctype, nodes.FuncType)
        self.assertIsInstance(func.body, nodes.BlockStmt)
        self.assertIsInstance(func.body.body[0], nodes.Decl)

        decl = func.body.body[0]
        self.assertIsInstance(decl._assign_expr, knodes.KcLookup)

        lookup = decl._assign_expr
        self.assertEqual(lookup.context, 'MyModule')
        self.assertEqual(lookup.member, 'some_variable')

unittest.main()
