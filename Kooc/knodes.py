from pyrser.parsing.node import Node
from cnorm import nodes

from weakref import ref

# Expression
#--------------------------------

class KcExpr(nodes.Expr):
    """Base for all kooc expressions"""

    def __init__(self):
        """
        expr_type (None | type | ref(type) | array of type): The expression type
        """
        Node.__init__(self)
        self.expr_type = None

class KcLookup(KcExpr):
    """Kooc type lookup"""

    def __init__(self, context, member):
        self.context = context
        self.member = member

class KcCall(KcExpr):
    """Kooc type/instance call node"""

    def __init__(self, context, function, params):
        self.context = context
        self.function = function
        self.params = params

# Top level
#--------------------------------

# FIXME: herite de nodes.BlockStmt ? non...
class KcTopLevel:
    pass

class KcImport(KcTopLevel):
    """@import node"""

    def __init__(self, file_name):
        self.file_name = file_name

# FIXME: use BlockStmt par composition ?
class KcModule(nodes.BlockStmt, KcTopLevel):
    """@module node"""

    def __init__(self, name):
        KcTopLevel.__init__(self)
        self.name = name

# FIXME: use BlockStmt par composition ?
class KcImplementation(nodes.BlockStmt, KcTopLevel):
    """@implementation node"""

    def __init__(self, name):
        KcTopLevel.__init__(self)
        self.name = name

class KcClass(KcModule):
    """@class node"""

    def __init__(self, name):
        KcModule.__init__(self, name)
        self.parents = {}

    def add_parent(self, parent): # FIXME: needed here ?
        if parent.name in self.parents:
            return True
        self.parents[parent.name] = ref(parent)

# Misc
#--------------------------------

class KcId(nodes.Id):
    """A kooc Id"""

