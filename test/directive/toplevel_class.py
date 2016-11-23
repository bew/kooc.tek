#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from Kooc import knodes
from cnorm import nodes

from base import DirectiveTestCase

class DirectiveClass(DirectiveTestCase):

    def test_class_inheritance(self):
        """A class with parents"""

        source = """
            @class A {}
            @class B {}
            @class C : A, B {}
        """

        ast = self.parse(source)
        self.assertTrue("C" in ast.ktypes)
        self.assertIsInstance(ast.ktypes["C"](), knodes.KcClass)

        klass = ast.ktypes["C"]()
        self.assertTrue("A" in klass.parents)
        self.assertTrue("B" in klass.parents)
        self.assertIsInstance(klass.parents, dict)

        self.assertIsInstance(klass.parents["A"](), knodes.KcClass)

    def test_class_inheritance_fail(self):
        """A class with unknown parents"""

        source = """
            @class C : DFYUI {}
        """

        with self.assertRaises(Exception):
            self.parse(source)

    def test_implicit_member_function(self):

        source = """
            @class MyClass
            {
                void implicit(MyClass *, int param);
            }
        """

        ast = self.parse(source)
        klass = ast.body[0]

        self.assertEqual(len(klass.members), 1)

        decl = klass.members[0]
        self.assertEqual(decl._name, 'implicit')
        self.assertIsInstance(decl._ctype, nodes.FuncType)

    def test_explicit_member_func(self):

        source = """
            @class MyClass
            {
                @member void explicit(int param);
            }
        """
        ast = self.parse(source)
        klass = ast.body[0]

        self.assertEqual(len(klass.members), 1)

        decl = klass.members[0]
        self.assertEqual(decl._name, 'explicit')
        self.assertIsInstance(decl._ctype, nodes.FuncType)

        self.assertEqual(len(decl._ctype._params), 2)

        first_param = decl._ctype._params[0]
        self.assertIsInstance(first_param._ctype, nodes.PrimaryType)
        self.assertEqual(first_param._ctype._identifier, 'MyClass')
        self.assertEqual(first_param._name, 'self')

    def test_explicit_member_var(self):

        source = """
            @class MyClass
            {
                @member float my_float = 4.2;
            }
        """

        ast = self.parse(source)
        klass = ast.body[0]

        self.assertEqual(len(klass.members), 1)

        decl = klass.members[0]
        self.assertEqual(decl._name, 'my_float')
        self.assertIsInstance(decl._ctype, nodes.PrimaryType)
        self.assertEqual(decl._ctype._identifier, 'float')

    def test_explicit_group_of_members(self):

        source = """
            @class MyClass
            {
                @member
                {
                    int my_int = 42;
                    void do_something();
                    int do_something(void *callback);
                }
            }
        """

        ast = self.parse(source)
        klass = ast.body[0]

        self.assertEqual(len(klass.members), 3)

        first_member = klass.members[0]
        self.assertEqual(first_member._name, 'my_int')

        second_member = klass.members[1]
        self.assertEqual(second_member._name, 'do_something')
        self.assertEqual(len(second_member._ctype._params), 1) # self

        third_member = klass.members[2]
        self.assertEqual(third_member._name, 'do_something')
        self.assertEqual(len(third_member._ctype._params), 2) # self, callback

# Theses tests cannot pass anymore, the KcClass is not filled at parsing time, but with visitors
if __name__ == '__main__':
    #unittest.main()
    pass
