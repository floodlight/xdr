:: from xdr.backends.python.utils import unpack_expr

:: if m.kind == "basic":
${dst} = ${unpack_expr(m)}
:: elif m.kind == "optional":
if unpacker.unpack_bool():
    ${dst} = ${unpack_expr(m)}
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
${dst} = unpacker.unpack_fopaque(${m.length})
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
${dst} = unpacker.unpack_opaque()
:: elif m.kind == "array":
${dst} = []
for i in xrange(0, ${m.length}):
    ${dst}.append(${unpack_expr(m)})
:: elif m.kind == "list":
_len = unpacker.unpack_int()
:: if m.length:
assert(_len <= ${m.length})
:: #endif
${dst} = []
for i in xrange(0, _len):
    ${dst}.append(${unpack_expr(m)})
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
