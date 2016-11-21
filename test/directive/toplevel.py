#!/usr/bin/env python3

import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from base import DirectiveTestCase

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

if __name__ == '__main__':
    unittest.main()
