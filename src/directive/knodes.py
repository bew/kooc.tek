from pyrser.parsing.node import Node
from cnorm import nodes

class KcModule(nodes.BlockStmt):
    """@module node"""

    def __init__(self, name):
        self.name = name

class KcImplementation(nodes.BlockStmt):
    """@implementation node"""

    def __init__(self, name):
        self.name = name

class KcClass:
    """@class node"""

    def __init__(self, name):
        self.name = name
        self.parents = {}
        #FIXME: more to do here ?

    def add_parent(self, parent):
        if parent.name in self.parents:
            return True
        self.parents[parent.name] = parent
        #TODO: check for incompatibilities with other parents ?
