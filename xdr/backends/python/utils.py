"""
Generate Python expressions to pack/unpack a given type

For basic types we directly call methods on the Packer/Unpacker. For
user-defined types (identifiers in the declaration grammar) we call
pack_into/unpack_from on a class with the given name. This works
whether the type is a struct, enum, union, or typedef.
"""

BASIC_TYPES = {
    'int' : 'int',
    'unsigned int': 'uint',
    'hyper': 'hyper',
    'unsigned hyper': 'uhyper',
    'float': 'float',
    'double': 'double',
    'bool': 'bool',
}

def pack_expr(m, src):
    if m.type in BASIC_TYPES:
        return "packer.pack_%s(%s)" % (BASIC_TYPES[m.type], src)
    else:
        return "%s.pack_into(packer, %s)" % (m.type, src)

def unpack_expr(m):
    if m.type in BASIC_TYPES:
        return "unpacker.unpack_%s()" % BASIC_TYPES[m.type]
    else:
        return "%s.unpack_from(unpacker)" % m.type

def literal(x, constants):
    if type(x) == str:
        assert x in constants
        return constants[x]
    else:
        return x
