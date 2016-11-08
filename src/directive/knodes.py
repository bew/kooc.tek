from pyrser.parsing.node import Node
from cnorm import nodes

class KcImport(Node):
    """@import node"""

    def __init__(self, filepath):
        self.filepath = filepath

class KcModule(Node):
    """@module node"""

    def __init__(self, name, block):
        self._name = name
        self.body = block

class KcImplementation(Node):
    """@implementation node"""

    def __init__(self, name, block):
        self._name = name
        self.body = block
