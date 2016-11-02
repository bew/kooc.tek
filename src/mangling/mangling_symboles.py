#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Virtual
DECORATOR_VIRTUAL = 'V'

# Origin of declaration
DECLARATION_FROM_MODULE = "MODULE"
DECLARATION_FROM_CLASS = "CLASS"
DECLARATION_FROM_INSTANCE = "OBJECT"

# Type Separator
BEGINTYPE_SEPARATOR = 'B'
ENDTYPE_SEPARATOR = 'E'

# Node Type
NODE_PRIMARYTYPE_CHAR = 'n'
NODE_COMPOSEDTYPE_CHAR = 'c'
NODE_FUNCTYPE_CHAR = 'f'
NODE_QUALTYPE_CHAR = 'q'
NODE_POINTERTYPE_CHAR = 'p'
NODE_ARRAYTYPE_CHAR = 'a'
NODE_NONETYPE_CHAR = 'o'
NODE_PARENTYPE_CHAR = 't'

# Nativ Types
NATIVTYPE_ELLIPSIS = 'Z'
NATIVTYPE_SIGNED_CHAR = 'C'
NATIVTYPE_CHAR = 'D'
NATIVTYPE_UNSIGNED_CHAR = 'E'
NATIVTYPE_SHORT_INT = 'F'
NATIVTYPE_UNSIGNED_SHORT_INT = 'G'
NATIVTYPE_INT = 'H'
NATIVTYPE_UNSIGNED_INT = 'I'
NATIVTYPE_LONG_INT = 'J'
NATIVTYPE_UNSIGNED_LONG_INT = 'K'
NATIVTYPE_FLOAT = 'M'
NATIVTYPE_DOUBLE = 'N'
NATIVTYPE_LONG_DOUBLE = 'O'
NATIVTYPE_VOID = 'X'

# Other Type
USERTYPE_TYPEDEF = 'T'
USERTYPE_ENUM = 'V'
USERTYPE_UNION = 'U'
USERTYPE_STRUCT = 'S'
USERTYPE_NATIV = 'W'

# Qualifier
QUALIFIER_CONST = 'c'
QUALIFIER_VOLATILE = 'l'

# Declaration Kind
DECLARATION_STATIC = 'S'
DECLARATION_AUTO =  'A'

#helper func
def format_mangling_string(format_string):
    return format_string.format(
        DECLARATION_STATIC = DECLARATION_STATIC,
        DECLARATION_AUTO = DECLARATION_AUTO,
        BEGINTYPE_SEPARATOR = BEGINTYPE_SEPARATOR,
        ENDTYPE_SEPARATOR = ENDTYPE_SEPARATOR,
        NODE_FUNCTYPE_CHAR = NODE_FUNCTYPE_CHAR,
        NODE_COMPOSEDTYPE_CHAR = NODE_COMPOSEDTYPE_CHAR,
        NODE_PRIMARYTYPE_CHAR = NODE_PRIMARYTYPE_CHAR,
        NODE_QUALTYPE_CHAR = NODE_QUALTYPE_CHAR,
        NODE_POINTERTYPE_CHAR = NODE_POINTERTYPE_CHAR,
        NODE_ARRAYTYPE_CHAR = NODE_ARRAYTYPE_CHAR,
        NODE_NONETYPE_CHAR = NODE_NONETYPE_CHAR,
        NODE_PARENTYPE_CHAR = NODE_PARENTYPE_CHAR,
        USERTYPE_TYPEDEF = USERTYPE_TYPEDEF,
        USERTYPE_ENUM = USERTYPE_ENUM,
        USERTYPE_UNION = USERTYPE_UNION,
        USERTYPE_STRUCT = USERTYPE_STRUCT,
        USERTYPE_NATIV  = USERTYPE_NATIV,
        QUALIFIER_CONST = QUALIFIER_CONST,
        QUALIFIER_VOLATILE = QUALIFIER_VOLATILE,
        NATIVTYPE_ELLIPSIS = NATIVTYPE_ELLIPSIS,
        NATIVTYPE_SIGNED_CHAR = NATIVTYPE_SIGNED_CHAR,
        NATIVTYPE_CHAR = NATIVTYPE_CHAR,
        NATIVTYPE_UNSIGNED_CHAR = NATIVTYPE_UNSIGNED_CHAR,
        NATIVTYPE_SHORT_INT = NATIVTYPE_SHORT_INT,
        NATIVTYPE_UNSIGNED_SHORT_INT = NATIVTYPE_UNSIGNED_SHORT_INT,
        NATIVTYPE_INT = NATIVTYPE_INT,
        NATIVTYPE_UNSIGNED_INT = NATIVTYPE_UNSIGNED_INT,
        NATIVTYPE_LONG_INT = NATIVTYPE_LONG_INT,
        NATIVTYPE_UNSIGNED_LONG_INT = NATIVTYPE_UNSIGNED_LONG_INT,
        NATIVTYPE_FLOAT = NATIVTYPE_FLOAT,
        NATIVTYPE_DOUBLE = NATIVTYPE_DOUBLE,
        NATIVTYPE_LONG_DOUBLE = NATIVTYPE_LONG_DOUBLE,
        NATIVTYPE_VOID = NATIVTYPE_VOID,
        DECLARATION_FROM_MODULE = DECLARATION_FROM_MODULE,
        DECLARATION_FROM_CLASS = DECLARATION_FROM_CLASS,
        DECLARATION_FROM_INSTANCE = DECLARATION_FROM_INSTANCE,
        DECORATOR_VIRTUAL = DECORATOR_VIRTUAL
    )
