from pyrser import meta
from cnorm import nodes
from Kooc import knodes

# TODO: rename visitor to 'all_exprs' ?

def yield_if_expr_rec(maybe_expr):
    if isinstance(maybe_expr, nodes.Expr) \
            and not isinstance(maybe_expr, nodes.Decl) \
            and not isinstance(maybe_expr, nodes.Id):
        yield maybe_expr
    if hasattr(maybe_expr, 'yield_expr'):
        for y in maybe_expr.yield_expr():
            yield y

# KOOC EXPR

@meta.add_method(knodes.KcLookup)
def yield_expr(self):
    if isinstance(self.context, nodes.Expr):
        for y in yield_if_expr_rec(self.context):
            yield y

@meta.add_method(knodes.KcCall)
def yield_expr(self):
    if isinstance(self.context, nodes.Expr):
        for y in yield_if_expr_rec(self.context):
            yield y

    for p in self.params:
        for y in yield_if_expr_rec(p):
            yield y

# EXPR

@meta.add_method(nodes.Func)
def yield_expr(self):
    for y in yield_if_expr_rec(self.call_expr):
        yield y
    for p in self.params:
        for y in yield_if_expr_rec(p):
            yield y

@meta.add_method(nodes.BlockInit)
def yield_expr(self):
    for expr in self.body:
        for y in yield_if_expr_rec(expr):
            yield y

@meta.add_method(nodes.BlockExpr)
def yield_expr(self):
    for expr in self.body:
        for y in yield_if_expr_rec(expr):
            yield y

# DECLARATION

@meta.add_method(nodes.Enumerator)
def yield_expr(self):
    for y in yield_if_expr_rec(self.expr):
        yield y

# decltype

@meta.add_method(nodes.DeclType)
def yield_expr(self):
    if self._decltype:
        self._decltype.yield_expr()

@meta.add_method(nodes.ArrayType)
def yield_expr(self):
    nodes.DeclType.yield_expr(self)
    for y in yield_if_expr_rec(self._expr):
        yield y

@meta.add_method(nodes.ParenType)
def yield_expr(self):
    nodes.DeclType.yield_expr(self)
    for p in self._params:
        for y in yield_if_expr_rec(p):
            yield y

# end decltype

@meta.add_method(nodes.FuncType)
def yield_expr(self):
    if self._decltype:
        self._decltype.yield_expr()
    for p in self._params:
        for y in yield_if_expr_rec(p):
            yield y

@meta.add_method(nodes.Decl)
def yield_expr(self):
    if hasattr(self, 'body'):
        for y in yield_if_expr_rec(self.body):
            yield y

    if hasattr(self, '_assign_expr'):
        for y in yield_if_expr_rec(self._assign_expr):
            yield y
    if hasattr(self, '_colon_expr'):
        for y in yield_if_expr_rec(self._colon_expr):
            yield y

# STATEMENT

@meta.add_method(nodes.Stmt)
def yield_expr(self):
    pass

@meta.add_method(nodes.ExprStmt)
def yield_expr(self):
    for y in yield_if_expr_rec(self.expr):
        yield y

@meta.add_method(nodes.BlockStmt)
def yield_expr(self):
    for p in self.body:
        for y in yield_if_expr_rec(p):
            yield y

@meta.add_method(nodes.Branch)
def yield_expr(self):
    for y in yield_if_expr_rec(self.expr):
        yield y

# conditions

@meta.add_method(nodes.Conditional)
def yield_expr(self):
    for y in yield_if_expr_rec(self.condition):
        yield y

@meta.add_method(nodes.If)
def yield_expr(self):
    nodes.Conditional.yield_expr(self)
    for y in yield_if_expr_rec(self.thencond):
        yield y
    for y in yield_if_expr_rec(self.elsecond):
        yield y

@meta.add_method(nodes.While)
def yield_expr(self):
    nodes.Conditional.yield_expr(self)
    for s in self.body:
        for y in yield_if_expr_rec(s):
            yield y

@meta.add_method(nodes.Switch)
def yield_expr(self):
    nodes.Conditional.yield_expr(self)
    for s in self.body:
        for y in yield_if_expr_rec(s):
            yield y

@meta.add_method(nodes.Do)
def yield_expr(self):
    nodes.Conditional.yield_expr(self)
    for s in self.body:
        for y in yield_if_expr_rec(s):
            yield y

@meta.add_method(nodes.For)
def yield_expr(self):
    for y in yield_if_expr_rec(self.init):
        yield y
    for y in yield_if_expr_rec(self.condition):
        yield y
    for y in yield_if_expr_rec(self.increment):
        yield y
    for s in self.body:
        for y in yield_if_expr_rec(s):
            yield y

# end conditions
