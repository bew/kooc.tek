#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from Kooc import knodes
from Kooc.directive import KParsingError

from base import DirectiveTestCase

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

        with self.assertRaises(KParsingError):
            self.parse(source)

if __name__ == '__main__':
    unittest.main()
