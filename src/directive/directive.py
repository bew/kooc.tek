from pyrser import meta
from pyrser.grammar import Grammar
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm import nodes


#TODO: change class names, archi
class Directive(Grammar, Declaration):
    entry = "translation_unit"
    grammar = """
        declaration = [
            Declaration.declaration
            |
            [
                #kc_is_top_level(current_block)
                kc_top_level :tl
                #end_decl(current_block, tl)
            ]
        ]

        kc_top_level = [
            [
                kc_at_import
                | kc_at_module
                | kc_at_implementation
            ] :>_
        ]

        kc_at_import = [
            "@import" string :name
            #kc_new_import(_, name)
        ]

        kc_at_module = [
            "@module" id :name
            kc_decl_block :block
            #kc_new_module(_, name, block)
        ]

        kc_at_implementation = [
            "@implementation" id :name
            kc_decl_block :block
            #kc_new_implementation(_, name, block)
        ]

        //TODO: rename... is it a kind of MangleBlock ?
        kc_decl_block = [
            '{'
                __scope__ :current_block
                #kc_new_decl_block(_, current_block)
                [
                    Declaration.declaration
                ]*
            '}'
        ]


        // ---- MANGLING ? -----
        // maybe this should be done later ?

        // TODO: overload 'declarator' (a Decl type) to check if we need to mangle a certain type

        /*
           TODO: overload 'identifier' (an Id type) to check if we need to mangle it, based
           on it's type ? or just his name... don't know.. If we have the identifier's Decl, we
           can get it's type, shouldn't be too hard..
        */

        f_or_v_id = [
            identifier :name
            #mangling(name)
        ]

    """

@meta.hook(Directive)
def mangling(self, nameNode):
    name = self.value(nameNode)
    return True


@meta.hook(Directive)
def kc_is_top_level(self, current_block):
    is_root = isinstance(current_block.ref, nodes.RootBlockStmt)
    return is_root


# KC import

class KcImport(Node):
    def __init__(self, filepath):
        self.filepath = filepath

@meta.hook(Directive)
def kc_new_import(self, ast, nameNode):
    str_with_quotes = self.value(nameNode)
    filepath = str_with_quotes[1:-1]
    ast.set(KcImport(filepath))
    return True


# KC module

class KcModule(Node):
    def __init__(self, name, block):
        self._name = name
        self.body = block

@meta.hook(Directive)
def kc_new_module(self, ast, nameNode, moduleBlockNode):
    ast.set(KcModule(self.value(nameNode), moduleBlockNode))
    return True


# KC implementation

class KcImplementation(Node):
    def __init__(self, name, block):
        self._name = name
        self.body = block

@meta.hook(Directive)
def kc_new_implementation(self, ast, nameNode, moduleBlockNode):
    ast.set(KcImplementation(self.value(nameNode), moduleBlockNode))
    return True


# KC decl block

class KcDeclBlock(nodes.RootBlockStmt):
    def __init__(self, block):
        nodes.RootBlockStmt.__init__(self, block)
        #TODO: add some fields



@meta.hook(Directive)
def kc_new_decl_block(self, ast, module_block):
    ast.set(KcDeclBlock([]))
    module_block.ref = ast

    # FIXME: need that ? it's for handles scoped types in block
    #parent = self.rule_nodes.parents
    #if (('current_block' in parent and hasattr(parent['current_block'].ref, 'types'))):
    #    module_block.ref.types = parent['current_block'].ref.types.new_child()
    return True


