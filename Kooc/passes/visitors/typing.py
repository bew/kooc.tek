from Kooc.passes import yield_expr
from Kooc import knodes
from cnorm import nodes

from . import KVisitorError, VisitorRunner

from weakref import ref

class Typing(VisitorRunner):

    def register(self):
        self.register_visitor(self.type_c_cast)
        # run full typing system here ?
        self.register_visitor(self.resolve_expr_context)

    def resolve_expr_context(self):
        for expr in self.ast.yield_expr():
            if not isinstance(expr, knodes.KcExpr): # limit to KcCall & KcLookup
                continue

            ctx = expr.context
            if isinstance(ctx, str):
                if ctx in self.ast.ktypes:
                    expr.context = self.ast.ktypes[ctx]
                    continue
                raise KVisitorError('KcExpr context "{}" is not a KType'.format(ctx))

            elif not isinstance(ctx, nodes.Expr):
                raise KVisitorError('KcExpr context is not a str or expr: {}'.format(ctx))

            # TODO: handle primary_expression as context


    def type_c_cast(self):
        for expr in self.ast.yield_expr():
            if not isinstance(expr, nodes.Cast):
                continue

            expr.expr_type = ref(expr.params[0])

