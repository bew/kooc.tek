from Kooc.utils import KError

class KVisitorError(KError):
    """There was an error when visiting AST"""

class VisitorRunner:
    """An object used to run visitors on a given AST"""

    def __init__(self):
        self.ast = None
        self.visitors = []

    def register_visitor(self, func):
        self.visitors.append(func)

    def run(self, ast):
        self.ast = ast
        for func in self.visitors:
            func()

    def register(self):
        raise Exception('Visitor ' + self.__class__.__name__ + ' has no \'register\' function')

from .linkchecks import LinkChecks
from .typing import Typing
from .builder import ClassBuilder

