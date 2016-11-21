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
from Kooc.passes import visitors
from Kooc.directive.typedliteral import TypedLiteral

class TypingTest(unittest.TestCase):
    """Base class for all typing tests"""

    parser = Directive()
    typed_literal = TypedLiteral()
    
    def test_param_Literal(self):
        """Resolve typing on one param with Literal node"""
        source = """
            @module Test
            {
                void funcInt(int var);
                void funcDouble(double var);
                void funcVoid();
            }

            int main()
            {
                [Test funcInt :42];
                [Test funcDouble :42.42];
                [Test funcVoid];
            }
        """

        print("\n~~~~~~~~~~ test_param_Literal ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcInt = ast.body[1].body.body[0].expr
        self.assertEqual(funcInt.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcInt.params[0].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param0 type

        # Check funcFloat
        funcDouble = ast.body[1].body.body[1].expr
        self.assertEqual(funcDouble.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcDouble.params[0].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param0 type

        # Check funcVoid
        funcVoid = ast.body[1].body.body[2].expr
        self.assertEqual(funcVoid.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type

        
    def test_params_Literal(self):
        """Resolve typing on multiple params with Literal node"""
        source = """
            @module Test
            {
                void funcIntDouble(int foo, double bar);
                void funcDoubleInt(double foo, int bar);
            }

            int main()
            {
                [Test funcIntDouble :42 :42.42];
                [Test funcDoubleInt :42.42 :42];
            }
        """

        print("\n~~~~~~~~~~ test_params_Literal ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcIntDouble = ast.body[1].body.body[0].expr
        self.assertEqual(funcIntDouble.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcIntDouble.params[0].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param0 type
        self.assertEqual(funcIntDouble.params[1].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param1 type

        # Check funcFloat
        funcDoubleInt = ast.body[1].body.body[1].expr
        self.assertEqual(funcDoubleInt.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcDoubleInt.params[0].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param0 type
        self.assertEqual(funcDoubleInt.params[1].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param1 type


    def test_param_Id(self):
        """Resolve typing on one param with Id node"""
        source = """
            @module Test
            {
                void funcInt(int var);
                void funcDouble(double var);
                void funcVoid();
            }

            int main()
            {
                int foo = 42;
                double bar = 42.42;

                [Test funcInt :foo];
                [Test funcDouble :bar];
                [Test funcVoid];
            }
        """


        print("\n~~~~~~~~~~ test_param_Id ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcInt = ast.body[1].body.body[2].expr
        self.assertEqual(funcInt.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcInt.params[0].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param0 type

        # Check funcFloat
        funcDouble = ast.body[1].body.body[3].expr
        self.assertEqual(funcDouble.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcDouble.params[0].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param0 type

        # Check funcVoid
        funcVoid = ast.body[1].body.body[4].expr
        self.assertEqual(funcVoid.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type


    def test_params_Id(self):
        """Resolve typing on multiple params with Id nodes"""
        source = """
            @module Test
            {
                void funcIntDouble(int foo, double bar);
                void funcDoubleInt(double foo, int bar);
            }

            int main()
            {
                int foo = 42;
                double bar = 42.42;

                [Test funcIntDouble :foo :bar];
                [Test funcDoubleInt :bar :foo];
            }
        """

        print("\n~~~~~~~~~~ test_params_Id ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcIntDouble = ast.body[1].body.body[2].expr
        self.assertEqual(funcIntDouble.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcIntDouble.params[0].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param0 type
        self.assertEqual(funcIntDouble.params[1].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param1 type

        # Check funcFloat
        funcDoubleInt = ast.body[1].body.body[3].expr
        self.assertEqual(funcDoubleInt.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcDoubleInt.params[0].expr_type.__dict__, nodes.PrimaryType("double").__dict__) # Function param0 type
        self.assertEqual(funcDoubleInt.params[1].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param1 type


    def test_param_KcLookup(self):
        """Resolve typing on one param with KcLookup node"""
        source = """
            @module Test
            {
                int foo = 42;
                double bar = 42.42;

                void funcInt(int var);
                void funcDouble(double var);
                void funcVoid();
            }

            int main()
            {
                [Test funcInt :[Test.foo]];
                [Test funcDouble :[Test.bar]];
                [Test funcVoid];
            }
        """


        print("\n~~~~~~~~~~ test_param_KcLookup ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcInt = ast.body[1].body.body[0].expr
        self.assertEqual(funcInt.expr_type.__dict__, nodes.PrimaryType("void").__dict__) # Function return type
        self.assertEqual(funcInt.params[0].expr_type.__dict__, nodes.PrimaryType("int").__dict__) # Function param0 type

        # # Check funcFloat
        funcDouble = ast.body[1].body.body[1].expr
        self.assertEqual(funcDouble.expr_type._identifier, nodes.PrimaryType("void")._identifier) # Function return type
        self.assertEqual(funcDouble.params[0].expr_type._identifier, nodes.PrimaryType("double")._identifier) # Function param0 type

        # Check funcVoid
        funcVoid = ast.body[1].body.body[2].expr
        self.assertEqual(funcVoid.expr_type._identifier, nodes.PrimaryType("void")._identifier) # Function return type


    def test_params_KcLookup(self):
        """Resolve typing on multiple params with KcLookup nodes"""
        source = """
            @module Test
            {
                int foo = 42;
                double bar = 42.42;

                void funcIntDouble(int foo, double bar);
                void funcDoubleInt(double foo, int bar);
            }

            int main()
            {
                [Test funcIntDouble :[Test.foo] :[Test.bar]];
                [Test funcDoubleInt :[Test.bar] :[Test.foo]];
            }
        """

        print("\n~~~~~~~~~~ test_params_KcLookup ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        # Check funcInt
        funcIntDouble = ast.body[1].body.body[0].expr
        self.assertEqual(funcIntDouble.expr_type._identifier, nodes.PrimaryType("void")._identifier) # Function return type
        self.assertEqual(funcIntDouble.params[0].expr_type, nodes.PrimaryType("int")) # Function param0 type
        self.assertEqual(funcIntDouble.params[1].expr_type, nodes.PrimaryType("double")) # Function param1 type

        # Check funcFloat
        funcDoubleInt = ast.body[1].body.body[1].expr
        self.assertEqual(funcDoubleInt.expr_type._identifier, nodes.PrimaryType("void")._identifier) # Function return type
        self.assertEqual(funcDoubleInt.params[0].expr_type._identifier, nodes.PrimaryType("double")._identifier) # Function param0 type
        self.assertEqual(funcDoubleInt.params[1].expr_type._identifier, nodes.PrimaryType("int")._identifier) # Function param1 type

    def test_param_Binary(self):
        """Resolve typing on param with Binary nodes"""
        source = """
            @module Test
            {
                void func(int var);
                void func(double var);
                void func();
            }

            int main()
            {
                [Test func :42+42];
                [Test func :42.42+42.42];
                [Test func];
            }
        """

        print("\n~~~~~~~~~~ test_param_Binary ~~~~~~~~~~\n")
        ast = self.parser.parse(source)
        runners = [
            visitors.linkchecks.LinkChecks(),
            visitors.typing.Typing()
            ]
        for runner in runners:
            runner.register();
            runner.run(ast)
            
        
    # def test_return(self):
    #     """Resolve typing on return"""
    #     source = """
    #         @module Test
    #         {
    #             int funcInt();
    #             float funcFloat();
    #             void funcVoid();
    #         }

    #         int main()
    #         {
    #             int foo = [Test funcInt :foo];
    #             float bar = [Test funcFloat :bar];
    #             [Test funcVoid];
    #         }
    #     """
        
    #     ast = self.parser.parse(source)
    #     runners = [
    #         visitors.linkchecks.LinkChecks(),
    #         visitors.typing.Typing()
    #         ]
    #     for runner in runners:
    #         runner.register();
    #         runner.run(ast)

            
if __name__ == '__main__':
    unittest.main()
