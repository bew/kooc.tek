from pyrser import meta
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm import nodes
from weakref import ref

from Kooc import knodes
from Kooc.utils import KError

class KParsingError(KError):
    """Class for parsing error"""


class Directive(Grammar, Declaration):
    entry = "translation_unit"
    grammar = """
        translation_unit = [
            @ignore("C/C++")
            [
                __scope__ :current_block
                #new_root(_, current_block)
                #kc_init_root(_)
                [
                    declaration
                ]*
            ]
            Base.eof
        ]

        // Kooc primary expression rules
        //--------------------------------

        primary_expression = [
            [ kc_primary_expression | Declaration.primary_expression ] :>_
        ]

        kc_primary_expression = [
            [ kc_cast | kc_expression ] :>_
        ]

        kc_cast = [
            "@!" '(' type_name :type ')' kc_expression :>_
            #kc_set_expr_type(_, type)
        ]

        // Kooc expression rules
        //--------------------------------

        kc_expression = [
            '[' [ kc_lookup | kc_call ] :>_ ']'
        ]

        kc_expr_context = [
            kc_id :id #kc_is_typename(id, current_block)
            | primary_expression
        ]

        // [Module.variable]
        // [Module.var1.subvar] Besoin de le gerer ? (later)
        kc_lookup = [
            kc_expr_context :ctx '.' kc_id :member
            #kc_set_lookup(_, ctx, member)
        ]

        // [Module function]
        // [Module function :param1 :param2]
        kc_call = [
            kc_expr_context :ctx kc_id :func kc_call_params :params
            #kc_set_call(_, ctx, func, params)
        ]

        kc_call_params = [
            #kc_call_params_init(_)
            [ ':' assignement_expression :expr #kc_call_params_add(_, expr) ]*
        ]

        // Kooc top level keyword rules
        //--------------------------------

        declaration = [
            #kc_is_top_level(current_block) kc_top_level
            | Declaration.declaration
        ]

        kc_top_level = [
            kc_at_import
            | kc_at_module
            | kc_at_implementation
            | kc_at_class
        ]

        kc_at_import = [
            "@import" Base.string :name
            #kc_new_import(current_block, name)
        ]

        kc_at_module = [
            "@module" kc_id :name
            Statement.compound_statement :block
            #kc_new_module(current_block, name, block)
        ]

        kc_at_implementation = [
            "@implementation" kc_id :name #kc_add_typename(current_block, name)
            kc_implem_block :block
            #kc_new_implementation(current_block, name, block)
        ]

        kc_implem_block = [
            '{'
                __scope__ :current_block #new_blockstmt(_, current_block)
                [
                    Declaration.declaration
                    | kc_at_member #kc_add_member(current_block)
                ]*
            '}'
        ]

        kc_at_class = [
            "@class" kc_id :class_name #kc_add_typename(current_block, class_name)
            __scope__ :inheritance_list
            [ ':' kc_class_inheritance :>inheritance_list ]?
            kc_class_block :block
            #kc_add_class(current_block, class_name, inheritance_list, block)
        ]

        // Kooc class rules
        //--------------------------------

        kc_class_inheritance = [
            kc_id :name #kc_inheritance_add_parent(_, name)
            [
                ',' kc_id :name #kc_inheritance_add_parent(_, name)
            ]*
        ]

        kc_class_block = [
            '{'
                __scope__ :current_block #new_blockstmt(_, current_block)
                [
                    Declaration.declaration #kc_check_member_func(class_name, current_block)
                    | kc_at_member #kc_add_member(current_block)
                    | kc_at_virtual #kc_add_virtual(current_block)
                ]*
            '}'
        ]

        kc_at_member = [
            "@member" [
                Declaration.declaration
                | block_of_declarations :bd #kc_add_to_body(bd, current_block)
            ]
        ]

        kc_at_virtual = [
            "@virtual" [
                Declaration.declaration
                | block_of_declarations :bd #kc_add_to_body(bd, current_block)
            ]
        ]

        // Misc rules
        //--------------------------------

        block_of_declarations = [
            '{'
                __scope__ :current_block #new_blockstmt(_, current_block)
                [ Declaration.declaration ]*
            '}'
        ]

        kc_id = [ @ignore('null') Base.id :id #kc_new_id(_, id) ]

    """

    def parse(self, source, cwd = '.'):
        self.cwd = cwd
        return Grammar.parse(self, source)

@meta.hook(Directive)
def kc_init_root(self, ast):
    setattr(ast, "ktypes", {})
    return True

# Checks hooks
#--------------------------------

@meta.hook(Directive)
def kc_is_top_level(self, current_block):
    is_root = isinstance(current_block.ref, nodes.RootBlockStmt)
    return is_root

# Expressions hooks
#--------------------------------

@meta.hook(Directive)
def kc_set_expr_type(self, expr, type_name):
    expr.expr_type = type_name._ctype
    return True

@meta.hook(Directive)
def kc_set_lookup(self, ast, ctx_node, member_node):
    ctx_name = self.value(ctx_node)
    member = self.value(member_node)
    ast.set(knodes.KcLookup(ctx_name, member))
    return True

@meta.hook(Directive)
def kc_set_call(self, ast, ctx_node, func_node, params_node):
    ctx_name = self.value(ctx_node)
    func_name = self.value(func_node)
    params = params_node.params
    ast.set(knodes.KcCall(ctx_name, func_name, params))
    return True

@meta.hook(Directive)
def kc_call_params_init(self, ast):
    setattr(ast, "params", [])
    return True

@meta.hook(Directive)
def kc_call_params_add(self, ast, expr):
    ast.params.append(expr)
    return True

# Top level hooks
#--------------------------------

@meta.hook(Directive)
def kc_new_import(self, current_block, name_node):
    # Form kheader path, header result
    module_path = self.value(name_node)[1:-1]


    if module_path.endswith('.kh'):
        header_path = module_path.replace('.kh', '.h')
    elif module_path.endswith('.kc'):
        raise KParsingError("Cannot import kooc source module")
    else:
        header_path = module_path + '.h'
        module_path = module_path + '.kh'

    module_fullpath = self.cwd + module_path

    current_block.ref.body.append(knodes.KcImport(module_fullpath, module_path))
    return True

@meta.hook(Directive)
def kc_new_module(self, current_block, name_node, module_block):
    module_name = self.value(name_node)
    knodes.KcModule.init_from_blockstmt(module_block, module_name)

    current_block.ref.ktypes[module_name] = ref(module_block)
    current_block.ref.body.append(module_block)
    return True

@meta.hook(Directive)
def kc_new_implementation(self, current_block, name_node, implem_block):
    knodes.KcImplementation.init_from_blockstmt(implem_block, self.value(name_node))
    current_block.ref.body.append(implem_block)
    return True

# Class hooks
#--------------------------------

@meta.hook(Directive)
def kc_add_typename(self, current_block, name_node):
    typename = self.value(name_node)

    # add this type in cnorm type system
    current_block.ref.types[typename] = True
    return True

@meta.hook(Directive)
def kc_is_typename(self, id_node, current_block):
    id = self.value(id_node)

    return id in current_block.ref.types


@meta.hook(Directive)
def kc_inheritance_add_parent(self, ast, name_node):
    if not hasattr(ast, "parents"):
        setattr(ast, "parents", [])

    parent_name = self.value(name_node)
    if parent_name not in ast.parents:
        ast.parents.append(parent_name)
    return True

@meta.hook(Directive)
def kc_add_class(self, current_block, name_node, inheritance_list, class_block):
    parents = []
    if hasattr(inheritance_list, "parents"):
        parents = inheritance_list.parents

    class_name = self.value(name_node)
    ktypes = current_block.ref.ktypes

    if class_name in ktypes:
        raise KParsingError("Class re-opening not supported")

    knodes.KcClass.init_from_blockstmt(class_block, class_name)
    klass = class_block

    # add parents
    for parent_name in parents:
        if parent_name not in ktypes:
            raise KParsingError("Unknown class parent type '%s'" % parent_name)

        klass.parents.append(parent_name)

    ktypes[class_name] = ref(klass)
    current_block.ref.body.append(klass)

    # C type for class:
    # ==== typedef kc_{class}_interface {class}; ====

    class_interface_struct_ctype = nodes.ComposedType('kc_' + class_name + '_interface')
    class_interface_struct_ctype._specifier = nodes.Specifiers.STRUCT
    class_interface_struct_ctype._storage = nodes.Storages.TYPEDEF
    klass.typedef = nodes.Decl(class_name, class_interface_struct_ctype)

    current_block.ref.types[class_name] = ref(klass.typedef)
    return True

@meta.hook(Directive)
def kc_check_member_func(self, class_name_node, current_block):
    class_name = self.value(class_name_node)

    def is_member_func(decl):
        # is a function declaration ?
        if not (isinstance(decl, nodes.Decl) and isinstance(decl._ctype, nodes.FuncType)):
            return False

        func_ctype = decl._ctype

        # has at least one param ?
        if not len(func_ctype._params) >= 1:
            return False

        first_param = func_ctype._params[0]

        # is PrimaryType ?
        if not (isinstance(first_param, nodes.Decl) and isinstance(first_param._ctype, nodes.PrimaryType)):
            return False

        first_ctype = first_param._ctype

        # is pointer ?
        if not (first_ctype._decltype and isinstance(first_ctype._decltype, nodes.PointerType)):
            return False

        # is single pointer ? (Something *, not Something **)
        if not first_ctype._decltype._decltype is None:
            return False

        # is pointer on current class ?
        return first_ctype._identifier == class_name

    last_decl = current_block.ref.body[-1]
    if is_member_func(last_decl):
        last_decl.__class__ = knodes.KcMethodDecl

    return True

@meta.hook(Directive)
def kc_add_member(self, current_block):
    last_decl = current_block.ref.body[-1]

    def setup_member(decl):
        if isinstance(decl._ctype, nodes.FuncType):
            decl.__class__ = knodes.KcMethodDecl
        else:
            decl.__class__ = knodes.KcMemberDecl

    if isinstance(last_decl, nodes.Decl):
        setup_member(last_decl)
        return True

    if isinstance(last_decl, nodes.BlockStmt):
        # remove block from body
        current_block.ref.body.pop()

        for decl in last_decl.body:
            setup_member(decl)

            # append each decl in body
            current_block.ref.body.append(decl)

        return True

    return False

@meta.hook(Directive)
def kc_add_virtual(self, current_block):
    last_decl = current_block.ref.body[-1]

    def setup_virtual(decl):
        if isinstance(decl._ctype, nodes.FuncType):
            decl.__class__ = knodes.KcVirtualDecl
        else:
            raise KParsingError('Cannot make a variable declaration virtual')

    if isinstance(last_decl, nodes.Decl):
        setup_virtual(last_decl)
        return True

    if isinstance(last_decl, nodes.BlockStmt):
        # remove block from body
        current_block.ref.body.pop()

        for decl in last_decl.body:
            setup_virtual(decl)

            # append each decl in body
            current_block.ref.body.append(decl)

        return True

    return False

# Misc hooks
#--------------------------------

@meta.hook(Directive)
def kc_new_id(self, ast, id_node):
    ast.set(knodes.KcId(self.value(id_node)))
    return True

@meta.hook(Directive)
def kc_add_to_body(self, block, current_block):
    current_block.ref.body.append(block)
    return True

# vim:ft=python.pyrser:
