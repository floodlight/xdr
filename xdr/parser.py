# This grammar is written using Pyparsing and closely follows the grammar in
# RFC 4506.
#
# Known differences with the standard:
#  - We don't allow inline struct, enum, and union definitions.
#  - The standard is inconsistent on whether identifiers are allowed as enum
#    values. We only support constants as enum values.

## Grammar

import pyparsing as P
from xdr.ir import *

kw = P.Keyword
s = P.Suppress
lit = P.Literal
g = P.Group

identifier = P.Word(P.alphanums, P.alphanums + '_').setName("identifier")

decimal_constant = P.Word('-123456789', '0123456789')
hexademical_constant = P.Combine('0x' - P.Word('0123456789abcdefABCDEF'))
octal_constant = P.Word('0', '01234567')

constant = (decimal_constant | hexademical_constant | octal_constant) \
    .setName("constant") \
    .setParseAction(lambda x: int(x[0], 0))

value = constant | identifier

type_specifier = \
    (P.Optional(kw("unsigned")) + kw("int")) | \
    (P.Optional(kw("unsigned")) + kw("hyper")) | \
    kw("float") | kw("double") | kw("quadruple") | kw("bool") | \
    identifier

declaration = \
    kw("void") | \
    kw("opaque") + identifier + lit("[") + value + lit("]") | \
    kw("opaque") + identifier + lit("<") + P.Optional(value) + lit(">") | \
    kw("string") + identifier + lit("<") + P.Optional(value) + lit(">") | \
    g(type_specifier) + identifier + lit("[") + value + lit("]") | \
    g(type_specifier) + identifier + lit("<") + P.Optional(value) + lit(">") | \
    g(type_specifier) + identifier | \
    g(type_specifier) + lit('*') + identifier

enum_body = s("{") + g(P.delimitedList(g(identifier + s('=') + constant))) + s("}")

struct_body = s("{") + P.OneOrMore(g(declaration + s(";"))) + s("}")

case_spec = g(s(kw("case")) - value + s(":") + g(declaration) + s(";"))
default_spec = g(kw('default') - s(':') + g(declaration) + s(';'))

union_body = \
    s(kw("switch")) - s("(") + g(declaration) + s(")") + s("{") + \
    g(P.OneOrMore(case_spec) + P.Optional(default_spec)) + \
    s("}")

constant_def = kw("const") - identifier + s("=") + constant + s(";")

type_def = \
    kw("typedef") - g(declaration) + s(";") | \
    kw("enum") - identifier + enum_body + s(";") | \
    kw("struct") - identifier + g(struct_body) + s(";") | \
    kw("union") - identifier + union_body + s(";")

definition = type_def | constant_def

specification = P.ZeroOrMore(g(definition))

specification.ignore(P.cStyleComment)

def parse_ast(src):
    """
    Given an input string, return the AST.
    """
    return specification.parseString(src, parseAll=True).asList()

def parse_declaration(x):
    if x[0] == 'void':
        return XDRDeclaration(None, 'basic', 'void', None)
    elif x[0] == 'opaque' or x[0] == 'string':
        type = x[0]
        name = x[1]
        kind = x[2] == '[' and 'array' or 'list'
        length = x[3]
        if length == '>':
            length = None
        return XDRDeclaration(name, kind, type, length)
    else:
        name = x[1]
        kind = 'basic'
        type = ' '.join(x[0])
        length = None
        if name == '*':
            name = x[2]
            kind = 'optional'
        elif len(x) > 2 and x[2] == '[':
            kind = 'array'
        elif len(x) > 2 and x[2] == '<':
            kind = 'list'
        if kind == 'array' or kind == 'list':
            length = x[3]
            if length == '>':
                length = None
        return XDRDeclaration(name, kind, type, length)

def parse_definition(x):
    if x[0] == 'struct':
        return XDRStruct(x[1], [parse_declaration(y) for y in x[2]])
    elif x[0] == 'enum':
        return XDREnum(x[1], [XDREnumMember(y[0], y[1]) for y in x[2]])
    elif x[0] == 'const':
        return XDRConst(x[1], x[2])
    elif x[0] == 'typedef':
        return XDRTypedef(parse_declaration(x[1]))
    elif x[0] == 'union':
        return XDRUnion(x[1], parse_declaration(x[2]),
                        [XDRUnionMember(y[0], parse_declaration(y[1])) for y in x[3]])

def parse(src):
    """
    Given an input string, return the IR.
    """
    ast = parse_ast(src)
    return [parse_definition(x) for x in ast]
