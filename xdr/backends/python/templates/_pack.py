:: # Given an XDRDeclaration 'm' and a source expression 'src', this template
:: # generates serialization code.
:: from xdr.backends.python.utils import pack_expr
::
:: if m.kind == "basic":
:: # Plain
:: # int x
${pack_expr(m, src)}
::
:: elif m.kind == "optional":
:: # Optional
:: # int *x
if ${src} is not None:
    packer.pack_bool(True)
    ${pack_expr(m, src)}
else:
    packer.pack_bool(False)
::
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
:: # Fixed length string
:: # string x[2]
packer.pack_fopaque(${m.length}, ${src})
::
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
:: # Variable length string
:: # string x<2>
:: if m.length is not None:
assert(len(${src}) <= ${m.length})
:: #endif
packer.pack_opaque(${src})
::
:: elif m.kind == "array":
:: # Fixed length array
:: # int x[2]
assert(len(${src}) == ${m.length})
for x in ${src}:
    ${pack_expr(m, 'x')}
::
:: elif m.kind == "list":
:: # Variable length array
:: # int x<2>
:: if m.length is not None:
assert(len(${src}) <= ${m.length})
:: #endif
packer.pack_int(len(${src}))
for x in ${src}:
    ${pack_expr(m, 'x')}
::
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
