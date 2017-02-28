from Kooc.passes import yield_expr
from Kooc import knodes
from cnorm import nodes
from Kooc.directive.typedliteral import TypedLiteral

from . import KVisitorError, VisitorRunner

from weakref import ref

# TODO:
#
# Take care of multiple KcLookup with same signature
# Invariance for KcCall and func
class Typing(VisitorRunner):

    typed_literal = TypedLiteral()
    ignored_expression = [nodes.Raw, nodes.PrimaryType]

    def register(self):
        """Register all the visitors for the runner"""
        self.register_visitor(self.resolve_expr_context)
        self.register_visitor(self.type_c_cast)
        self.register_visitor(self.resolve)
        self.register_visitor(self.check_and_apply)


    def resolve(self):
        """Resolve all the invariance possibilities"""
        for expr in self.ast.yield_expr():
            self.choose_resolve_method(expr)


    def resolve_KcCall(self, kccall_expr):
        """Resolve the typing for a KcCall node"""
        if (self.is_typed(kccall_expr)):
            return kccall_expr

        kccall_expr.params = self.resolve_params(kccall_expr.params)
        kccall_expr_type = list()
        kccall_name = kccall_expr.function

        # Search among the context the KcCall declarations by it's name
        for decl in kccall_expr.context().body:
            if isinstance(decl, nodes.Decl) is not True or isinstance(decl._ctype, nodes.FuncType) is not True:
                continue
            elif decl._name == kccall_name and len(decl._ctype.params) == len(kccall_expr.params) and self.compare_params_type_KcCall(kccall_expr.params, decl._ctype.params) is True:
                kccall_expr_type.append(nodes.PrimaryType(decl._ctype._identifier))

        # Check if at least a type has been found and set them
        if len(kccall_expr_type) <= 0:
            raise KVisitorError("Cant find any definition of KcCall '"+ kccall_name +"'") # TODO : Precise the params as criteria for search
        else:
            if len(kccall_expr_type) == 1:
                kccall_expr.expr_type = kccall_expr_type[0]
            else:
                kccall_expr.expr_type = kccall_expr_type

        if isinstance(kccall_expr.expr_type, list) is not True:
            kccall_expr = self.set(kccall_expr, kccall_expr.expr_type)

        return kccall_expr


    def resolve_KcLookup(self, kclookup_expr):
        """Resolve the typing for KcLookup node"""
        if self.is_typed(kclookup_expr) is True:
            return kclookup_expr

        kclookup_expr_type = list()
        kclookup_name = kclookup_expr.member

        # Search among the context the KcLookup declarations by it's name and add the expr_type found
        for decl in kclookup_expr.context().body:
            if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                continue
            elif decl._name == kclookup_name:
                kclookup_expr_type.append(nodes.PrimaryType(decl._ctype._identifier))

        # Check if at least a type has been found and set them
        if len(kclookup_expr_type) <= 0:
            raise KVisitorError("Cant find any definition of KcLookup '"+ kclookup_name +"'")
        else:
            if len(kclookup_expr_type) == 1:
                kclookup_expr.expr_type = kclookup_expr_type[0]
            else:
                kclookup_expr.expr_type = kclookup_expr_type

        return kclookup_expr


    def resolve_Literal(self, literal_expr):
        """Resolve the typing for Literal node"""
        return self.typed_literal.parse(literal_expr.value)


    def resolve_Id(self, id_expr):
        """Resolve the typing for an Id node"""
        if (self.is_typed(id_expr)):
            return id_expr

        id_expr_type = None
        id_name = id_expr.value

        # Search among all declaration the id declaration by it's name
        root = self.get_root(id_expr)
        while root is not None:
            for decl in root.body:
                if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                    continue
                elif decl._name == id_name:
                    if id_expr_type is None:
                        id_expr_type = nodes.PrimaryType(decl._ctype._identifier)
                    else:
                        raise KVisitorError("Multiple definition of Id for the same signature for '"+ id_name +"'")
            root = self.get_root(root)

        # Check if a type has been found and set it
        if id_expr_type is None:
            # we are in a function ? search in func params
            root = self.get_root(id_expr)
            while root is not None:
                if hasattr(root, 'parent') and root.parent():
                    parent = root.parent()
                    if hasattr(parent, '_ctype') and isinstance(parent._ctype, nodes.FuncType):
                        params = parent._ctype.params
                        for decl in params:
                            if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                                continue
                            elif decl._name == id_name:
                                id_expr_type = nodes.PrimaryType(decl._ctype._identifier)


                root = self.get_root(root)

            if id_expr_type is None:
                raise KVisitorError("Cant find any definition of Id '"+ id_name +"'")
            else:
                id_expr.expr_type = id_expr_type

        else:
            id_expr.expr_type = id_expr_type

        return id_expr


    def resolve_Binary(self, binary_expr):
        """Resolve the typing for a Binary node"""
        if (self.is_typed(binary_expr)):
            return binary_expr

        binary_expr.params = self.resolve_params(binary_expr.params)
        binary_expr.expr_type = self.get_matches_expr_type(binary_expr.params[0].expr_type, binary_expr.params[1].expr_type)

        if isinstance(binary_expr.expr_type, list) is not True:
            binary_expr = self.set(binary_expr, binary_expr.expr_type)

        return binary_expr


    def resolve_Ternary(self, ternary_expr):
        """Resolve the typing for a Ternary node"""
        if (self.is_typed(ternary_expr)):
            return ternary_expr

        ternary_expr.params = self.resolve_params(ternary_expr.params)
        ternary_expr.expr_type = self.get_matches_expr_type(ternary_expr.params[1].expr_type, ternary_expr.params[2].expr_type)

        if isinstance(ternary_expr.expr_type, list) is not True:
            ternary_expr = self.set(ternary_expr, ternary_expr.expr_type)

        return ternary_expr


    def resolve_Paren_Unary(self, paren_unary_expr):
        """Resolve the typing for a Paren or a Unary node"""
        if (self.is_typed(paren_unary_expr)):
            return paren_unary_expr

        paren_unary_expr.params = self.resolve_params(paren_unary_expr.params)
        paren_unary_expr.expr_type = paren_unary_expr.params[0].expr_type

        if isinstance(paren_unary_expr.expr_type, list) is not True:
            paren_unary_expr = self.set(paren_unary_expr, paren_unary_expr.expr_type)

        return paren_unary_expr


    def resolve_Func(self, func_expr):
        """Resolve the typing for an Func node"""
        if (self.is_typed(func_expr)):
            return func_expr

        func_expr_type = None
        func_name = func_expr.call_expr.value

        # Search among all declaration the func declaration by it's name
        root = self.get_root(func_expr)
        while root is not None:
            for decl in root.body:
                if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                    continue
                elif decl._name == func_name:
                    if func_expr_type is None:
                        func_expr_type = nodes.PrimaryType(decl._ctype._identifier)
                    else:
                        raise KVisitorError("Multiple definition of Func for the same signature for '"+ func_name +"'")
            root = self.get_root(root)

        # Check if a type has been found and set it
        if func_expr_type is None:
            raise KVisitorError("Cant find any definition of Func '"+ func_name +"'")
        else:
            func_expr.expr_type = func_expr_type

        if isinstance(func_expr.expr_type, list) is not True:
            func_expr = self.set(func_expr, func_expr.expr_type)
            
        return func_expr


    def set(self, expr, expr_type):
        """Choose the way to set the typing by type of node"""
        if isinstance(expr, knodes.KcCall):
            return self.set_KcCall(expr, expr_type)
        elif isinstance(expr, knodes.KcLookup):
            return self.set_KcLookup(expr, expr_type)
        elif isinstance(expr, nodes.Binary):
            return self.set_Binary(expr, expr_type)
        elif isinstance(expr, nodes.Ternary):
            return self.set_Ternary(expr, expr_type)
        elif isinstance(expr, nodes.Paren) or isinstance(expr, nodes.Unary):
            return self.set_Paren_Unary(expr, expr_type)
        elif isinstance(expr, nodes.Func):
            return self.set_Func(expr, expr_type)
        else:
            return expr


    def set_KcCall(self, kccall_expr, expr_type):
        kccall_expr.expr_type = expr_type
        already_typed = False
        
        for decl in kccall_expr.context().body:
            if isinstance(decl, nodes.Decl) is not True or isinstance(decl._ctype, nodes.FuncType) is not True:
                continue
            elif decl._name == kccall_expr.function and len(decl._ctype.params) == len(kccall_expr.params) and decl._ctype._identifier == kccall_expr.expr_type._identifier and self.compare_params_type_KcCall(kccall_expr.params, decl._ctype.params) is True:
                if already_typed is False:
                    already_typed = True
                    for key, param in enumerate(kccall_expr.params):
                        kccall_expr.params[key] = self.set(param, decl._ctype._params[key]._ctype)
                else:
                    raise KVisitorError("Multiple type spotted !!")
                        
        return kccall_expr


    def set_KcLookup(self, kclookup_expr, expr_type):
        kclookup_expr.expr_type = expr_type
        return kclookup_expr


    def set_Binary(self, binary_expr, expr_type):
        binary_expr.expr_type = expr_type
        binary_expr.params[0] = self.set(binary_expr.params[0], expr_type)
        binary_expr.params[1] = self.set(binary_expr.params[1], expr_type)
        return binary_expr


    def set_Ternary(self, ternary_expr, expr_type):
        ternary_expr.expr_type = expr_type
        ternary_expr.params[1] = self.set(ternary_expr.params[1], expr_type)
        ternary_expr.params[2] = self.set(ternary_expr.params[2], expr_type)
        return ternary_expr


    def set_Paren_Unary(self, paren_unary_expr, expr_type):
        paren_unary_expr.expr_type = expr_type
        paren_unary_expr.params[0] = self.set(paren_unary_expr.params[0], expr_type)
        return paren_unary_expr


    def set_Func(self, func_expr, expr_type):
        func_name = func_expr.call_expr.value

        root = self.get_root(func_expr)
        while root is not None:
            for decl in root.body:
                if isinstance(decl, nodes.Decl) is not True or hasattr(decl, "_name") is not True:
                    continue

                elif decl._name == func_name and func_expr.expr_type._identifier == decl._ctype._identifier and len(func_expr.params) == len(decl._ctype.params):
                    for key, param in enumerate(func_expr.params):
                        func_expr.params[key] = self.set(param, decl._ctype._params[key]._ctype)
                    break
            root = self.get_root(root)


        return func_expr

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
        elif isinstance(expr, nodes.Paren) or isinstance(expr, nodes.Unary):
            return self.resolve_Paren_Unary(expr)
        elif isinstance(expr, nodes.Func):
            return self.resolve_Func(expr)
        elif type(expr) not in self.ignored_expression:
            raise KVisitorError("Unknow way to resolve expression: "+ expr.__class__.__name__)


    def is_typed(self, expr):
        """Check if the typing is already done"""
        if hasattr(expr, "expr_type") is True and isinstance(expr.expr_type, nodes.PrimaryType):
            return True
        else:
            return False


    def resolve_params(self, params):
        """Resolve the types of the params"""
        for key, param in enumerate(params):
            params[key] = self.choose_resolve_method(param)
        return params


    def get_root(self, expr):
        """Get the root (BlockStmt) from the given expression by accessing the parents"""
        if isinstance(expr, nodes.RootBlockStmt):
            return None
        root = expr.parent()
        while isinstance(root, nodes.BlockStmt) is not True:
            root = root.parent()
        return root


    def compare_params_type_KcCall(self, kccall_params, decl_params):
        """Compare if the params are the same between a KcCall and a Decl"""
        for key, decl_param in enumerate(decl_params):
            kccall_param_expr_type = kccall_params[key].expr_type
            if isinstance(kccall_param_expr_type, list) is not True:
                if kccall_param_expr_type.__dict__ != decl_param._ctype.__dict__:
                    return False
            else:
                is_equal = False
                for kcall_param_sub_expr_type in kccall_param_expr_type:
                    if kcall_param_sub_expr_type.__dict__ == decl_param._ctype.__dict__:
                        is_equal = True
                if is_equal is False:
                    return False
        return True


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


    def get_matches_expr_type_lists(self, first_expr_type_list, second_expr_type_list):
        """Get the matches expression_type between two list of expression_type"""
        expr_type = list()
        for sub_first_expr_type in first_expr_type_list:
            for sub_second_expr_type in second_expr_type_list:
                if sub_first_expr_type.__dict__ == sub_second_expr_type.__dict__:
                    expr_type.append(sub_first_expr_type)

        if len(expr_type) <= 0:
            raise KVisitorError("The both expr_type don't have any match")
        else:
            if len(expr_type) == 1:
                return expr_type[0]
            else:
                return expr_type


    def get_matches_expr_type_list(self, first_expr_type, second_expr_type_list):
        """Get the matches expression_type between an expression_type and a list of expression_type"""
        expr_type = None
        for sub_second_expr_type in second_expr_type_list:
            if first_expr_type.__dict__ == sub_second_expr_type.__dict__:
                if expr_type is not None:
                    raise KVisitorError("Multiple type is not authorized")
                else:
                    expr_type = first_expr_type

        if expr_type is None:
            raise KVisitorError("The both expr_type don't have any match")
        else:
            return expr_type


    def get_matches_expr_type(self, first_expr_type, second_expr_type):
        """Get the matches expression_type between two expression_type (can be list)"""
        if isinstance(first_expr_type, list) is True and isinstance(second_expr_type, list) is True:
            return self.get_matches_expr_type_lists(first_expr_type, second_expr_type)
        elif isinstance(first_expr_type, list) is True:
            return self.get_matches_expr_type_list(second_expr_type, first_expr_type)
        elif isinstance(second_expr_type, list) is True:
            return self.get_matches_expr_type_list(first_expr_type, second_expr_type)
        else:
            if first_expr_type.__dict__ != second_expr_type.__dict__:
                raise KVisitorError("The both expr_type don't have any match")
            else:
                return first_expr_type


    # ~~~~~~~~~~ Shit of Lesell ~~~~~~~~~~

    def resolve_expr_context(self):
        for expr in self.ast.yield_expr():
            if not isinstance(expr, knodes.KcExpr): # limit to KcCall & KcLookup
                continue

            ctx = expr.context
            if isinstance(ctx, str):
                ctx = ctx.strip()
                if ctx in self.ast.ktypes:
                    expr.context = self.ast.ktypes[ctx]
                    continue
                raise KVisitorError('KcExpr context "{}" is not a KType'.format(ctx))

            elif not isinstance(ctx, nodes.Expr):
                raise KVisitorError('KcExpr context is not a str or expr: {}'.format(ctx))

            
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
