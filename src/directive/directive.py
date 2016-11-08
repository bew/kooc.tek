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
            Statement.compound_statement :block
            #kc_new_module(_, name, block)
        ]

        kc_at_implementation = [
            "@implementation" id :name
            Statement.compound_statement :block
            #kc_new_implementation(_, name, block)
        ]

        // TODO: work here:
        /*
        kc_class_block = [
            '{'
                __scope__:current_block
                #new_blockstmt(_, current_block)
                [
                    line_of_code
                    | "@member" '{' des trucs '}'
                ]*
            '}'
        ]
        //*/

    """

@meta.hook(Directive)
def kc_is_top_level(self, current_block):
    is_root = isinstance(current_block.ref, nodes.RootBlockStmt)
    return is_root

@meta.hook(Directive)
def kc_new_import(self, ast, nameNode):
    str_with_quotes = self.value(nameNode)
    filepath = str_with_quotes[1:-1]
    ast.set(KcImport(filepath))
    return True

@meta.hook(Directive)
def kc_new_module(self, ast, nameNode, blockNode):
    ast.set(KcModule(self.value(nameNode), blockNode))
    return True

@meta.hook(Directive)
def kc_new_implementation(self, ast, nameNode, blockNode):
    ast.set(KcImplementation(self.value(nameNode), blockNode))
    return True

# vim:ft=python.pyrser:
