
from Kooc.utils import KError

from Kooc.passes import yield_expr
from Kooc import knodes

from cnorm import nodes
from weakref import ref

class KVisitorError(KError):
    """There was an error when visiting AST"""

class VisitorRunner:
    """An object used to run visitors on a given AST"""

    def __init__(self, ast):
        self.ast = ast

    def bind_implem(self):
        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcImplementation):
                continue

            # find corresponding type (module/class)
            if tl.name in self.ast.ktypes:
                # bind implem to type
                tl.bind_mc = self.ast.ktypes[tl.name]
            else:
                raise KVisitorError('Cannot find KType "{}", available KTypes: {}'.format(tl.name, self.ast.ktypes.keys()))


    def resolve_expr_context(self):

        for expr in self.ast.yield_expr():
            if not isinstance(expr, knodes.KcExpr): # limit to KcCall & KcLookup
                continue
            print(">>>>> Got KcExpr from yield:", expr.__class__.__name__)

            ctx = expr.context
            if isinstance(ctx, str):
                if ctx in self.ast.ktypes:
                    expr.context = self.ast.ktypes[ctx]
                    continue
                raise KVisitorError('KcExpr context "{}" is not a KType'.format(ctx))

            else:
                raise KVisitorError('KcExpr context is not a str: {}'.format(ctx))


    def type_c_cast(self):
        print('Trying to find some C Cast')

        for expr in self.ast.yield_expr():
            if not isinstance(expr, nodes.Cast):
                continue

            print('>>>>> Found C Cast:', expr)
            expr.expr_type = ref(expr.params[0])

        print('End of trying to find some C Cast')

