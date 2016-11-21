import unittest
import sys, os

filePath = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, filePath + '/../..')

from Kooc.directive import Directive

class DirectiveTestCase(unittest.TestCase):
    """Base class for all Directive test cases"""

    koocparser = Directive()

    def parse(self, source : str):
        """Parse the given source"""

        return self.koocparser.parse(source)

    def parse_in_block(self, source_in_block : str):
        """Parse source as code in a block (ex: in a function)"""

        source = " { " + source_in_block + " } "

        ast = self.parse(source)
        ast_in_block = ast.body[0].body
        return ast_in_block

