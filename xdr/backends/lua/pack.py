"""
Determine the function to call to pack/unpack a given type
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

def packer(type):
    if type in BASIC_TYPES:
        return "write_%s" % BASIC_TYPES[type]
    else:
        return "public.write_%s" % type

def unpacker(type):
    if type in BASIC_TYPES:
        return "read_%s" % BASIC_TYPES[type]
    else:
        return "public.read_%s" % type

def literal(x, constants):
    if x is None:
        return "nil"
    elif type(x) == str:
        assert x in constants
        return constants[x]
    else:
        return x
