:: # Given an XDRDeclaration 'm' and a destination variable 'dst', this template
:: # generates deserialization code.
:: from xdr.backends.python.utils import unpack_expr
::
:: if m.kind == "basic":
:: # Plain
:: # int x
${dst} = ${unpack_expr(m)}
::
:: elif m.kind == "optional":
:: # Optional
:: # int *x
if unpacker.unpack_bool():
    ${dst} = ${unpack_expr(m)}
::
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
:: # Fixed length string
:: # string x[2]
${dst} = unpacker.unpack_fopaque(${m.length})
::
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
:: # Variable length string
:: # string x<2>
${dst} = unpacker.unpack_opaque()
::
:: elif m.kind == "array":
:: # Fixed length array
:: # int x[2]
${dst} = []
for i in xrange(0, ${m.length}):
    ${dst}.append(${unpack_expr(m)})
::
:: elif m.kind == "list":
:: # Variable length array
:: # int x<2>
_len = unpacker.unpack_int()
:: if m.length:
assert(_len <= ${m.length})
:: #endif
${dst} = []
for i in xrange(0, _len):
    ${dst}.append(${unpack_expr(m)})
::
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
