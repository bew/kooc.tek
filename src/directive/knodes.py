from pyrser.parsing.node import Node
from cnorm import nodes

class KcModule(nodes.BlockStmt):
    """@module node"""

    def __init__(self, name):
        self._name = name

class KcImplementation(nodes.BlockStmt):
    """@implementation node"""

    def __init__(self, name):
        self._name = name
