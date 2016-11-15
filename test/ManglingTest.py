#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys, os

from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/..')

from Kooc.mangling.full import Mangler as FullMangler

class ManglingTest(unittest.TestCase):
    """Allow to check if the mangling is conform to the documentation"""

    cparse = Declaration()
    mangler = FullMangler()

    # Module part
    def test_var_from_module(self):
        """Test if a var is correctly mangle from a module"""
        declaration = "int i;"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_o___E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_var_storage_static_from_module(self):
        """Test if a static var is correctly mangle from a module"""
        declaration = "static int i;"
        moduleName = "Test"
        solution = "S_B_n_W_H_B_o___E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    # def test_var_storage_extern_from_module(self):
    #     """Test if a extern var is correctly mangle from a module"""
    #     declaration = "extern int i;"
    #     moduleName = "Test"
    #     solution = "S_B_n_W_H_B_o___E_E_MODULE_4_Test_1_i"

    #     ast = self.cparse.parse(declaration);
    #     mangled = ""
    #     for index, decl in enumerate(ast.body):
    #         mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

    #     self.assertEqual(mangled, solution)

    def test_var_qualifier_const_from_module(self):
        """Test if a const var is correctly mangle from a module"""
        declaration = "const int i;"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_q_c_B_o___E_E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_var_qualifier_volatile_from_module(self):
        """Test if a volatile var is correctly mangle from a module"""
        declaration = "volatile int i;"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_q_l_B_o___E_E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_var_pointer_from_module(self):
        """Test if a pointer var is correctly mangle from a module"""
        declaration = "int *i;"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_p__B_o___E_E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_var_pointer_qualifier_const_from_module(self):
        """Test if a const pointer var is correctly mangle from a module"""
        declaration = "const int *i;"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_p__B_q_c_B_o___E_E_E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_var_array_from_module(self):
        """Test if an array var is correctly mangle from a module"""
        declaration = "int i[1];"
        moduleName = "Test"
        solution = "A_B_n_W_H_B_a__B_o___E_E_E_MODULE_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)


    def test_function_without_parameters_from_module(self):
        """Test if a function without parameters is correctly mangle from a module"""
        declaration = "void foo();"
        moduleName = "Test"
        solution = "A_B_f_W_X_B_o___E_E_MODULE_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_function_with_one_parameter_from_module(self):
        """Test if a function with one parameter is correctly mangle from a module"""
        declaration = "void foo(float bar);"
        moduleName = "Test"
        solution = "A_B_n_W_M_B_o___E_E_B_f_W_X_B_o___E_E_MODULE_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    def test_function_with_multiple_parameters_from_module(self):
        """Test if a function with multiple parameters is correctly mangle from a module"""
        declaration = "void foo(float bar, int baz, long qux);"
        moduleName = "Test"
        solution = "A_B_n_W_M_B_o___E_E_B_n_W_H_B_o___E_E_B_n_W_J_B_o___E_E_B_f_W_X_B_o___E_E_MODULE_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_module(decl._name, decl._ctype, moduleName)

        self.assertEqual(mangled, solution)

    # Class part
    def test_var_from_class(self):
        """Test if a var is correctly mangle from a class"""
        declaration = "int i;"
        className = "Test"
        solution = "A_B_n_W_H_B_o___E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_var_storage_static_from_class(self):
        """Test if a static var is correctly mangle from a class"""
        declaration = "static int i;"
        className = "Test"
        solution = "S_B_n_W_H_B_o___E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    # def test_var_storage_extern_from_class(self):
    #     """Test if a extern var is correctly mangle from a class"""
    #     declaration = "extern int i;"
    #     className = "Test"
    #     solution = "S_B_n_W_H_B_o___E_E_CLASS_4_Test_1_i"

    #     ast = self.cparse.parse(declaration);
    #     mangled = ""
    #     for index, decl in enumerate(ast.body):
    #         mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

    #     self.assertEqual(mangled, solution)

    def test_var_qualifier_const_from_class(self):
        """Test if a const var is correctly mangle from a class"""
        declaration = "const int i;"
        className = "Test"
        solution = "A_B_n_W_H_B_q_c_B_o___E_E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_var_qualifier_volatile_from_class(self):
        """Test if a volatile var is correctly mangle from a class"""
        declaration = "volatile int i;"
        className = "Test"
        solution = "A_B_n_W_H_B_q_l_B_o___E_E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_var_pointer_from_class(self):
        """Test if a pointer var is correctly mangle from a class"""
        declaration = "int *i;"
        className = "Test"
        solution = "A_B_n_W_H_B_p__B_o___E_E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_var_pointer_qualifier_const_from_class(self):
        """Test if a const pointer var is correctly mangle from a class"""
        declaration = "const int *i;"
        className = "Test"
        solution = "A_B_n_W_H_B_p__B_q_c_B_o___E_E_E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_var_array_from_class(self):
        """Test if an array var is correctly mangle from a class"""
        declaration = "int i[1];"
        className = "Test"
        solution = "A_B_n_W_H_B_a__B_o___E_E_E_CLASS_4_Test_1_i"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)


    def test_function_without_parameters_from_class(self):
        """Test if a function without parameters is correctly mangle from a class"""
        declaration = "void foo();"
        className = "Test"
        solution = "A_B_f_W_X_B_o___E_E_CLASS_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_function_with_one_parameter_from_class(self):
        """Test if a function with one parameter is correctly mangle from a class"""
        declaration = "void foo(float bar);"
        className = "Test"
        solution = "A_B_n_W_M_B_o___E_E_B_f_W_X_B_o___E_E_CLASS_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

    def test_function_with_multiple_parameters_from_class(self):
        """Test if a function with multiple parameters is correctly mangle from a class"""
        declaration = "void foo(float bar, int baz, long qux);"
        className = "Test"
        solution = "A_B_n_W_M_B_o___E_E_B_n_W_H_B_o___E_E_B_n_W_J_B_o___E_E_B_f_W_X_B_o___E_E_CLASS_4_Test_3_foo"

        ast = self.cparse.parse(declaration);
        mangled = ""
        for index, decl in enumerate(ast.body):
            mangled = self.mangler.mangle_class(decl._name, decl._ctype, className)

        self.assertEqual(mangled, solution)

unittest.main()
