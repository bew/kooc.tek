from pyrser.parsing.node import Node
from cnorm import nodes

# Expression
#--------------------------------

class KcExpr(Node):
    """Node for all kooc expressions"""

class KcCast(KcExpr):
    """@!(type)[expr] node"""

    def __init__(self, typ, expr):
        self.type = typ
        self.expr = expr

class KcLookup(KcExpr):
    """TODO: doc"""

    def __init__(self, context, member):
        self.context = context
        self.member = member

class KcCall(KcExpr):
    """TODO: doc"""

    def __init__(self, context, function, params):
        self.context = context
        self.function = function
        self.params = params

# Top level
#--------------------------------

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
