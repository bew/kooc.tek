from Kooc.passes import yield_expr
from Kooc import knodes
from cnorm import nodes
from Kooc.directive.typedliteral import TypedLiteral

from . import KVisitorError, VisitorRunner

from weakref import ref

class Typing(VisitorRunner):

    typed_literal = TypedLiteral()
    ignored_expression = [nodes.Raw]
    
    def register(self):
        """Register all the visitors for the runner"""
        self.register_visitor(self.type_c_cast)
        self.register_visitor(self.resolve_expr_context)
        self.register_visitor(self.resolve)
        self.register_visitor(self.check_and_apply)

        
    def resolve(self):
        """Resolve all the invariance possibilities"""
        for expr in self.ast.yield_expr():
            self.choose_resolve_method(expr)

            
    def resolve_KcCall(self, kccall_expr):
        """Resolve the typing for a KcCall node"""
        # Check if the typing is already done
        if hasattr(kccall_expr, "expr_type") is True and isinstance(kccall_expr.expr_type, list):
            return kccall_expr
        
        kccall_expr.params = self.resolve_params(kccall_expr.params)
        kccall_expr_type = list()
        kccall_name = kccall_expr.function

        # Search among the context the KcCall declarations by it's name
        for decl in kccall_expr.context().body:
            if isinstance(decl, nodes.Decl) is not True or isinstance(decl._ctype, nodes.FuncType) is not True:
                continue
            elif decl._name == kccall_name and len(decl._ctype.params) == len(kccall_expr.params) and self.compare_params_type(kccall_expr.params, decl._ctype.params) is True:
                kccall_expr_type.append(nodes.PrimaryType(decl._ctype._identifier))

        # Check if at least a type has been found and set them
        if len(kccall_expr_type) <= 0:
            raise KVisitorError("Cant find KcLookup '"+ kccall_name +"' for typing") # TODO : Precise the params as criteria for search
        else:
            kccall_expr.expr_type = kccall_expr_type
            
        return kccall_expr

                    
    def resolve_KcLookup(self, kclookup_expr):
        """Resolve the typing for KcLookup node"""
        # Check if the typing is already done
        if hasattr(kclookup_expr, "expr_type") is True and isinstance(kclookup_expr.expr_type, list):
            return kclookup_expr

        kclookup_expr_type = list()
        kclookup_name = kclookup_expr.member
        
        # Search among the context the KcLookup declarations by it's name
        for decl in kclookup_expr.context().body:
            if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                continue
            elif decl._name == kclookup_name:
                kclookup_expr_type.append(nodes.PrimaryType(decl._ctype._identifier))

        # Check if at least a type has been found and set them
        if len(kclookup_expr_type) <= 0:
            raise KVisitorError("Cant find KcLookup '"+ kclookup_name +"' for typing")
        else:
            kclookup_expr.expr_type = kclookup_expr_type
            
        return kclookup_expr

    
    def resolve_Literal(self, literal_expr):
        """Resolve the typing for Literal node"""
        return self.typed_literal.parse(literal_expr.value)

    
    def resolve_Id(self, id_expr):
        """Resolve the typing for an Id node"""
        # Check if the typing is already done
        if hasattr(id_expr, "expr_type") is True and isinstance(id_expr.expr_type, nodes.PrimaryType):
            return id_expr

        id_expr_type = None
        id_name = id_expr.value

        # Search among all declaration the id declaration by it's name
        for decl in self.get_root(id_expr).body:
            if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                continue
            elif decl._name == id_name:
                if id_expr_type is None:
                    id_expr_type = nodes.PrimaryType(decl._ctype._identifier)
                else:
                    raise KVisitorError("Ambiguous Id '"+ id_name +"' for typing")
                    
        # Check if a type has been found and set it
        if id_expr_type is None:
            raise KVisitorError("Cant find Id '"+ id_name +"' for typing")
        else:
            id_expr.expr_type = id_expr_type
            
        return id_expr


    def resolve_Binary(self, binary_expr):
        """Resolve the typing for a Binary node"""
        # Check if the typing is already done
        if hasattr(binary_expr, "expr_type") is True and isinstance(binary_expr.expr_type, nodes.PrimaryType):
            return binary_expr
        
        binary_expr.params = self.resolve_params(binary_expr.params)

        # Check if the both operands are of the same type. TODO : Handle in case of multiple types
        if binary_expr.params[0].expr_type.__dict__ != binary_expr.params[1].expr_type.__dict__:
            raise KVisitorError("The params of the binary node don't have the same type")
        else:
            binary_expr.expr_type = binary_expr.params[0].expr_type
            
        return binary_expr

    
    def resolve_Ternary(self, ternary_expr):
        """Resolve the typing for a Ternary node"""
        # Check if the typing is already done
        if hasattr(ternary_expr, "expr_type") is True and isinstance(ternary_expr.expr_type, nodes.PrimaryType):
            return ternary_expr

        ternary_expr.params = self.resolve_params(ternary_expr.params)

        # Check if the both operands are of the same type. TODO : Handle in case of multiple types
        if ternary_expr.params[1].expr_type.__dict__ != ternary_expr.params[2].expr_type.__dict__:
            raise KVisitorError("The params of the ternary node don't have the same type")
        else:
            ternary_expr.expr_type = ternary_expr.params[1].expr_type

        return ternary_expr
    
    
    # ~~~~~~~~~~ Utils ~~~~~~~~~~

    def choose_resolve_method(self, expr):
        """Choose the way to resolve the typing by type of node"""
        if isinstance(expr, knodes.KcCall):
            return self.resolve_KcCall(expr)
        elif isinstance(expr, knodes.KcLookup):
            return self.resolve_KcLookup(expr)
        elif isinstance(expr, nodes.Literal):
            return self.resolve_Literal(expr)
        elif isinstance(expr, nodes.Id):
            return self.resolve_Id(expr)
        elif isinstance(expr, nodes.Binary):
            return self.resolve_Binary(expr)
        elif isinstance(expr, nodes.Ternary):
            return self.resolve_Ternary(expr)
        elif type(expr) not in self.ignored_expression:
            raise KVisitorError("Unknow way to resolve expression: "+ expr.__class__.__name__)

        
    def get_root(self, expr):
        """Get the root (BlockStmt) from the given expression by accessing the parents"""
        root = expr.parent()
        while isinstance(root, nodes.BlockStmt) is not True:
            root = root.parent()
        return root


    def compare_params_type(self, kccall_params, decl_params):
        """Compare if the params are the same types on the two given list of params"""
        is_equal = True
        for key, decl_param in enumerate(decl_params):
            kccall_param_expr_type = kccall_params[key].expr_type[0] if isinstance(kccall_params[key].expr_type, list) else kccall_params[key].expr_type # TODO : Fixme :( => Invariance
            if kccall_param_expr_type._identifier != decl_param._ctype._identifier:
                is_equal = False
        return is_equal
            
    
    def resolve_params(self, params):
        """Resolve the types of the params"""
        for key, param in enumerate(params):
            params[key] = self.choose_resolve_method(param)
        return params


    def check_and_apply(self):
        for expr in self.ast.yield_expr():
            self.check_and_apply_loop(expr)

            
    def check_and_apply_loop(self, expr):
        if hasattr(expr, "expr_type") is True:
            if isinstance(expr.expr_type, list) is True:
                if len(expr.expr_type) > 1:
                    raise KVisitorError("Multiple type spotted !!")
                else:
                    expr.expr_type = expr.expr_type[0]
                    if hasattr(expr, "params"):
                        for key, param in enumerate(expr.params):
                            expr.params[key] = self.check_and_apply_loop(param)
            elif expr.expr_type is None:
                raise KVisitorError("No type spotted !!")
        return expr



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



    # where to resolve as a parent:
    # kccall
    # binary
    # ternary

    # missing
    # unary
    # paren
    # func
