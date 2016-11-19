# vim:ft=python.pyrser:

from pyrser import meta
from pyrser.grammar import Grammar
from cnorm import nodes
from cnorm.parsing.literal import Literal
from Kooc import knodes

class TypedLiteral(Grammar, Literal):
    """Parser to type a C literal"""

    entry = "typed_literal"
    grammar = """
        typed_literal = [ @ignore('null')
            Literal.double_const :val #kc_new_literal_double(_, val)
            | [
                Literal.hexadecimal_const_int
                | Literal.octal_const
                | Literal.decimal_const
            ] :val #kc_new_literal_int(_, val)
            | Literal.string_const :val #kc_new_literal_string(_, val)
            | Literal.char_const :val #kc_new_literal_char(_, val)
        ]

    """

@meta.hook(TypedLiteral)
def kc_new_literal_int(self, ast, val):
    ast.set(knodes.KcTypedLiteral(self.value(val), nodes.PrimaryType('int')))
    return True

@meta.hook(TypedLiteral)
def kc_new_literal_double(self, ast, val):
    ast.set(knodes.KcTypedLiteral(self.value(val), nodes.PrimaryType('double')))
    return True

@meta.hook(TypedLiteral)
def kc_new_literal_string(self, ast, val):
    string_type = nodes.PrimaryType('char')
    string_type.push(nodes.PointerType())

    ast.set(knodes.KcTypedLiteral(self.value(val), string_type))
    return True

@meta.hook(TypedLiteral)
def kc_new_literal_char(self, ast, val):
    ast.set(knodes.KcTypedLiteral(self.value(val), nodes.PrimaryType('char')))
    return True
