from pyrser import meta
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm import nodes

from knodes import *


#TODO: change class names, archi
class Directive(Grammar, Declaration):
    entry = "translation_unit"
    grammar = """
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
            "@implementation" kc_id :name
            Statement.compound_statement :block
            #kc_new_implementation(current_block, name, block)
        ]

        kc_at_class = [
            "@class" kc_id :name #kc_add_typename(current_block, name)
            __scope__ :inheritance_list
            [ ':' kc_class_inheritance :>inheritance_list ]?
            kc_class_block :block
            #kc_add_class(name, inheritance_list, block)
        ]

        kc_class_inheritance = [
            kc_id :name #kc_inheritance_add_parent(_, name)
            [
                ',' kc_id :name #kc_inheritance_add_parent(_, name)
            ]*
        ]

        kc_class_block = [
            '{'
                __scope__ :current_block
                #new_blockstmt(_, current_block)
                [
                    Declaration.declaration
                    | kc_at_member
                    | kc_at_virtual
                ]*
            '}'
        ]

        kc_at_member = [
            "@member" [
                Declaration.declaration | Statement.compound_statement
            ] #kc_add_member(current_block)
        ]

        kc_at_virtual = [
            "@virtual" Declaration.declaration #kc_add_virtual(current_block)
        ]

        kc_id = [ Base.id ]

    """

    def __init__(self):
        Grammar.__init__(self)
        self.imports = []
        self.typenames = []

@meta.hook(Directive)
def kc_is_top_level(self, current_block):
    is_root = isinstance(current_block.ref, nodes.RootBlockStmt)
    return is_root

@meta.hook(Directive)
def kc_new_import(self, current_block, name_node):
    if not hasattr(current_block.ref, "imports"):
        setattr(current_block.ref, "imports", [])

    module_path = self.value(name_node)[1:-1]

    if module_path.endswith('.kh'):
        header_path = module_path.replace('.kh', '.h')
    elif module_path.endswith('.kc'):
        # TODO: use custom Exception classes
        raise Exception("Cannot import kooc source module")
    else:
        header_path = module_path + '.h'
        module_path = module_path + '.kh'

    if module_path in current_block.ref.imports:
        return True
    else:
        current_block.ref.imports.append(module_path)

    inc = """#include "%s";""" % header_path
    raw = nodes.Raw(inc)
    current_block.ref.body.append(raw)
    return True

@meta.hook(Directive)
def kc_new_module(self, current_block, name_node, module_block):
    KcModule.__init__(module_block, self.value(name_node))
    module_block.__class__ = KcModule
    current_block.ref.body.append(module_block)
    return True

@meta.hook(Directive)
def kc_new_implementation(self, current_block, name_node, implem_block):
    KcImplementation.__init__(implem_block, self.value(name_node))
    implem_block.__class__ = KcImplementation
    current_block.ref.body.append(implem_block)
    return True

# Class hooks

@meta.hook(Directive)
def kc_add_typename(self, current_block, name_node):
    if not hasattr(current_block.ref, "typenames"):
        setattr(current_block.ref, "typenames", [])

    typename = self.value(name_node)
    if typename not in self.typenames:
        current_block.ref.typenames.append(typename)
    return True

@meta.hook(Directive)
def kc_inheritance_add_parent(self, ast, name_node):
    if not hasattr(ast, "parents"):
        setattr(ast, "parents", [])

    parent_name = self.value(name_node)
    if parent_name not in ast.parents:
        ast.parents.append(parent_name)
    return True

@meta.hook(Directive)
def kc_add_class(self, name_node, inheritance_list, class_block):
    # handle class re-opening ?
    # => check inheritance_list equality
    # or
    # => check that the re-opening does not mention an inheritance_list
    # or
    # => just don't care, and add the new inheritance_list to the existing one (if any) ?
    return True

@meta.hook(Directive)
def kc_add_member(self, current_block):
    return True

@meta.hook(Directive)
def kc_add_virtual(self, current_block):
    return True

# vim:ft=python.pyrser:
