from Kooc.passes import yield_expr
from Kooc import knodes
from cnorm import nodes
from Kooc.directive.typedliteral import TypedLiteral

from . import KVisitorError, VisitorRunner

from weakref import ref

class Typing(VisitorRunner):

    typed_literal = TypedLiteral()
    
    def register(self):
        """Register all the visitors for the runner"""
        self.register_visitor(self.type_c_cast)
        self.register_visitor(self.resolve_expr_context)
        self.register_visitor(self.resolve_invariance)
        self.register_visitor(self.check_and_apply)

        
    def resolve_invariance(self):
        """Resolve all the invariance possibilities"""
        for expr in self.ast.yield_expr():
            self.choose_resolve_method_invariance(expr)

            
    def resolve_invariance_KcCall(self, expr):
        """Resolve the invariance of a node of type KcCall"""
        expr.params = self.resolve_params(expr.params)
        
        context = expr.context()
        for decl in context.body:
            if isinstance(decl, nodes.Decl) is not True or isinstance(decl._ctype, nodes.FuncType) is not True:
                continue
            elif decl._name == expr.function and len(decl._ctype.params) == len(expr.params):
                is_equal = True
                for key, param in enumerate(decl._ctype.params):
                    if self.compare_param_type(param, expr.params[key]) is not True:
                        is_equal = False
                        break
                if is_equal is True:
                    expr.expr_type = [nodes.PrimaryType(decl._ctype._identifier)]

                    
    def resolve_invariance_KcLookup(self, expr):
        """Resolve the invariance of a node of type KcLookup"""
        if (expr.expr_type is not None):
            return
        context = expr.context()
        for decl in context.body:
            if isinstance(decl, nodes.Decl) is not True or isinstance(decl._ctype, nodes.FuncType) is True:
                continue
            elif decl._name == expr.member:
                expr.expr_type = [nodes.PrimaryType(decl._ctype._identifier)]
        return expr

    
    def resolve_invariance_Literal(self, expr):
        """Resolve the invariance of a node of type Literal"""
        return self.typed_literal.parse(expr.value)

    
    def resolve_invariance_Id(self, expr):
        """Resolve the invariance of a node of type Id"""
        root = self.get_root(expr)
        for decl in root.body:
            if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                continue
            elif decl._name == expr.value:
                expr.expr_type = [nodes.PrimaryType(decl._ctype._identifier)]
                break;
        # TODO : Raise error if id is not found
        return expr


    def check_and_apply(self):
        for expr in self.ast.yield_expr():
            self.check_and_apply_loop(expr)
            
    def check_and_apply_loop(self, expr):
        if hasattr(expr, "expr_type") is True and isinstance(expr.expr_type, list) is True:
            if len(expr.expr_type) > 1:
                print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO") # Todo handle error if multiple type
            else:
                expr.expr_type = expr.expr_type[0]
                if hasattr(expr, "params"):
                    for key, param in enumerate(expr.params):
                        expr.params[key] = self.check_and_apply_loop(param)
        return expr

    # ~~~~~~~~~~ Utils ~~~~~~~~~~

    def choose_resolve_method_invariance(self, expr):
        """Choose the way to resolve the invariance by type of node"""
        if isinstance(expr, knodes.KcCall):
            return self.resolve_invariance_KcCall(expr)
        elif isinstance(expr, knodes.KcLookup):
            return self.resolve_invariance_KcLookup(expr)
        elif isinstance(expr, nodes.Literal):
            return self.resolve_invariance_Literal(expr)
        elif isinstance(expr, nodes.Id):
            return self.resolve_invariance_Id(expr)
        else:
            print("Unknow way to resolve expression: "+ expr.__class__.__name__)
            return expr

        
    def get_root(self, expr):
        """Get the root (BlockStmt) from the given expression by accessing the parents"""
        root = expr.parent()
        while isinstance(root, nodes.BlockStmt) is not True:
            root = root.parent()
        return root


    def compare_param_type(self, param_decl, expr_decl):
        return param_decl == expr_decl

    
    def resolve_params(self, params):
        """Resolve the types of the params"""
        for key, param in enumerate(params):
            params[key] = self.choose_resolve_method_invariance(param)
        return params


    # ~~~~~~~~~~ Shit of Lesell ~~~~~~~~~~
    
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


    def get_types(self, ast):
        def get_single_type(from_t):
            if isinstance(from_t, weakref.ref):
                return from_t()
            return from_t

        assert(ast.expr_type is not None)
        t = ast.expr_type

        if isinstance(t, list):
            types = []
            for sub_t in t:
                types.append(get_single_type(sub_t))
                return types

        return get_single_type(t)
