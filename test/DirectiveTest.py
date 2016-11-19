#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys, os

from cnorm import nodes

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/..')

from Kooc.directive import Directive
from Kooc.chief import Koocer
from Kooc import knodes

class DirectiveTestCase(unittest.TestCase):
    """Base class for all Directive test cases"""

    koocparser = Directive(Koocer)

    def parse(self, source : str):
        """Parse the given source"""

        return self.koocparser.parse(source)

    def parse_in_block(self, source_in_block : str):
        """Parse source as code in a block (ex: in a function)"""

        source = " { " + source_in_block + " } "

        ast = self.parse(source)
        ast_in_block = ast.body[0].body
        return ast_in_block

class DirectiveTopLevel(DirectiveTestCase):

    def test_top_level(self):
        """@ Kooc keywords must be in top level only"""

        source = """
            {
                @module Bla
                {
                }
            }
        """

        with self.assertRaises(Exception):
            self.parse(source)


class DirectiveImport(DirectiveTestCase):

    def test_single_import(self):
        """Detect import statement"""

        source = """
            @import "myheader.kh"
        """

        ast = self.parse(source)
        kc_import = ast.body[0]
        self.assertIsInstance(kc_import, knodes.KcImport)
        self.assertEqual(kc_import.file_name, "myheader.kh")

    def test_multiple_import(self):
        """Detect multiple import statement"""

        source = """
            @import "myheader.kh"
            @import "myheader.kh"
            @import "otherheader.kh"
        """

        ast = self.parse(source)

        kc_import = ast.body[0]
        self.assertIsInstance(kc_import, knodes.KcImport)

        kc_import = ast.body[1]
        self.assertIsInstance(kc_import, knodes.KcImport)

    def test_import_kc(self):
        """Do not import kooc source file"""

        source = """
            @import "source.kc"
        """

        #TODO: use custom exception
        with self.assertRaises(Exception):
            self.parse(source)

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

class DirectiveTypes(DirectiveTestCase):

    def test_typenames_no_class(self):
        """No typename for a module"""

        source = """
            @module Bla {}
        """

        ast = self.parse(source)
        self.assertListEqual(ast.ktypenames, [])

    def test_typenames_for_class(self):
        """A class add a new typename"""

        source = """
            @class C {}
        """

        ast = self.parse(source)
        self.assertListEqual(ast.ktypenames, ["C"])

    def test_typenames_for_multi_classes(self):
        """typenames for class parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        ast = self.parse(source)
        self.assertListEqual(ast.ktypenames, ["A", "B", "C"])

class DirectiveClass(DirectiveTestCase):

    def test_class_inheritance(self):
        """A class with parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        # TODO: enable class testing
        return

        ast = self.parse(source)
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

        # TODO: enable class testing
        return

        with self.assertRaises(Exception):
            self.parse(source)

    #TODO: tests on virtuals, members, ........

class DirectiveLookup(DirectiveTestCase):

    def test_simple_in_top_level(self):
        """TODO: doc"""

        source = """
            int var = [MyModule.some_variable];
        """

        ast = self.parse(source)
        self.asserts_for_simple(ast)

    def test_simple_in_block(self):
        """TODO: doc"""

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

class DirectiveCall(DirectiveTestCase):

    def test_static_call(self):
        """TODO: doc"""

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

        self.assertIsInstance(kexpr.expr_type, nodes.Decl)
        self.assertEqual(kexpr.expr_type._ctype._identifier, 'int')

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
        self.assertIsInstance(kexpr.expr_type, nodes.Decl)
        self.assertEqual(kexpr.expr_type._ctype._identifier, 'int')

    def test_cannot_cast_non_kooc_expr(self):
        """Parsing must fails on Kooc casting a non Kooc expression"""

        source = """
            int a = @!(int)4;
        """

        with self.assertRaises(Exception):
            self.parse(source)

if __name__ == '__main__':
    unittest.main()
