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
