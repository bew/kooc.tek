#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os

from cnorm.parsing.declaration import Declaration
from cnorm.nodes import Decl
from cnorm.passes import to_c

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/..')

from Kooc.mangling import mangling
from Kooc.mangling.mangling_symboles import format_mangling_string

class ManglingTest:
    """Allow to check if the mangling is conform to the documentation"""

    cparse = Declaration()
    okString = '[\033[92mPASSED\033[0m]'
    failString = '[\033[91mFAILED\033[0m]'
    tests = {}

    def add_test(self, test_name, c_string, expected_mangling, origin, origin_name, expected_unmangling = None, context = [], is_virtual = False):
        """
        Add a test to the pool

        :param test_name: name of the test, to pass to run member function
        :type test_name: string
        :param c_string: c declaration, including the ';'
        :type c_string: string
        :param expected_mangling: the mangling that should be producued from c_string
        :type expected_mangling: string
        :param origin: the origin of the c_string declaration
        :type origin: mangling.DECLARATION_FROM_[MODULE|INSTANCE|OBJECT]
        :param origin_name: the name of the class|module th declaration is from
        :type origin_name: string
        :param expected_unmangling: the c declaration to expect from demangling 'expected_mangling'. Usefull only if significantly different from c_string.
        :type expected_unmangling: string
        :param context: c declaration that from which c_string depend.
        :type context: string array
        :param is_virtual: specify if the expression should be considered virtual
        :type is_virtual: bool
        """

        if test_name in self.tests:
            raise Exception('Test {} has already been added'.format(test_name))
        self.tests[test_name] = {
            'c_string': c_string,
            'expected_mangling': expected_mangling,
            'origin': origin,
            'origin_name': origin_name,
            'is_virtual': is_virtual,
            'context': context
        }
        if expected_unmangling != None:
            self.tests[test_name]['expected_unmangling'] = expected_unmangling

    def run_all(self):
        """ Run all the test in the pool """
        for test_name in self.tests.keys():
            self.run(test_name)

    def run(self, test_name):
        """
        Run a single test

        :param test_name: a test name already specified to add_test
        :type test_name: string
        """
        if not (test_name in self.tests):
            raise Exception('Test {} does not exist'.format(test_name))
        c_body = ''
        for context in self.tests[test_name]['context']:
            c_body += context
        c_body += self.tests[test_name]['c_string']
        c_ast = ''
        origin_c_string = ''
        try:
            c_ast = self.cparse.parse(c_body)
            origin_c_string = c_ast.body[len(self.tests[test_name]['context'])].to_c()
        except Exception as e:
            self._print_assert_equal(test_name, '\n' + str(e), None, 'Parsing for \'' + test_name + '\' : [' + '{result}' + ']')
            return
        mangled = ''
        unmangled = ''
        try:
            mangled = mangling.mangle(
                c_ast.body[len(self.tests[test_name]['context'])],
                self.tests[test_name]['origin'],
                self.tests[test_name]['origin_name'],
                virtual = self.tests[test_name]['is_virtual']
            )._name
        except Exception as e:
            self._print_assert_equal(test_name, e, None, 'Mangling for \'{name}\' : {result}')
            return
        try:
            unmangled = mangling.unmangle(mangled).decl.to_c()
        except Exception as e:
            self._print_assert_equal(test_name, e, None, 'Unmangling for \'{name}\' : {result}')
            return
        self._print_assert_equal(test_name, mangled, self.tests[test_name]['expected_mangling'], 'Mangling for \'{name}\' : {result}')
        if 'expected_unmangling' in self.tests[test_name]:
            self._print_assert_equal(test_name, str(unmangled).replace('\n', ''), self.tests[test_name]['expected_unmangling'], 'Unmangling for \'{name}\' : {result}')
        else:
            self._print_assert_equal(test_name, str(unmangled), str(origin_c_string), 'Unmangling for \'{name}\' : {result}')
        return

    def _print_assert_equal(self, test_name, arg1, arg2,  format_string):
        """
        print format_string and arg1 arg2, depnding of the result of arg1 == arg2

        :param arg1: whatever you expect to be equal to arg2
        :type arg1: whaterver you want
        :param arg2: whatever you expect to be equal to arg1
        :type arg2: whaterver you want
        :param format_string: format_string to print, may expect the following key : 'result'
        :type format_string: string ready for format. Can include the 'result' key.
        """
        # python format() cannot space pad align string @v@
        print(format_string.format(
            name = test_name,
            result = (self.okString if arg1 == arg2 else self.failString))
        )
        if arg1 != arg2:
            print('\tExpecting : ' + (arg2 if isinstance(arg2, str) else repr(arg2)))
            print('\tHad       : ' + (arg1 if isinstance(arg1, str) else repr(arg1)));

unit_test = ManglingTest()
unit_test.add_test(
    'simple native variable declaration',
    'int variable;',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.add_test(
    'simple native variable declaration from class',
    'int variable;',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_CLASS}_4_TEST_8_variable'
    ),
    mangling.OriginIsClass,
    'TEST'
)

unit_test.add_test(
    'static native variable declaration',
    'static int variable;',
    format_mangling_string(
        '{DECLARATION_STATIC}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.add_test(
    'virtual static native variable declaration',
    'static int variable;',
    format_mangling_string(
        '{DECORATOR_VIRTUAL}_{DECLARATION_STATIC}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST',
    is_virtual = True
)

unit_test.add_test(
    'usertype variable declaration',
    'toto variable;',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_TYPEDEF}_4_toto_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST',
    context = ['typedef int toto;']
)

unit_test.add_test(
    'pointer declaration',
    'void *variable;',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_VOID}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_POINTERTYPE_CHAR}__' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.add_test(
    'array declaration',
    'int variable[42];',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_ARRAYTYPE_CHAR}__' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST',
    expected_unmangling= 'int variable[];'
)

unit_test.add_test(
    'const pointer on unsigned long declaration',
    'const unsigned long *variable;',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_UNSIGNED_LONG_INT}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_POINTERTYPE_CHAR}__' +
        '{BEGINTYPE_SEPARATOR}_{NODE_QUALTYPE_CHAR}_{QUALIFIER_CONST}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.add_test(
    'function pointer with ellipsis declaration',
    'void (*variable)(int, ...);',
    format_mangling_string(
        '{DECLARATION_AUTO}_{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_VOID}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_POINTERTYPE_CHAR}__' +
        '{BEGINTYPE_SEPARATOR}_{NODE_PARENTYPE_CHAR}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_ELLIPSIS}_{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_variable'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.add_test(
    'function with ellipsis declaration',
    'void function(int, ...);',
    format_mangling_string(
        '{DECLARATION_AUTO}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_INT}_{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_PRIMARYTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_ELLIPSIS}_{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_' +
        '{BEGINTYPE_SEPARATOR}_{NODE_FUNCTYPE_CHAR}_{USERTYPE_NATIV}_{NATIVTYPE_VOID}_{BEGINTYPE_SEPARATOR}_{NODE_NONETYPE_CHAR}___' +
        '{ENDTYPE_SEPARATOR}_{ENDTYPE_SEPARATOR}_{DECLARATION_FROM_MODULE}_4_TEST_8_function'
    ),
    mangling.OriginIsModule,
    'TEST'
)

unit_test.run_all()
