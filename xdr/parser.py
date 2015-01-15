# This grammar is written using Pyparsing and closely follows the grammar in
# RFC 4506.
#
# Known differences with the standard:
#  - We don't allow inline struct, enum, and union definitions.
#  - The standard is inconsistent on whether identifiers are allowed as enum
#    values. We only support constants as enum values.

## Grammar

import pyparsing as P

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

case_spec = g(g(P.OneOrMore(s(kw("case")) - value + s(":"))) + g(declaration) + s(";"))
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
