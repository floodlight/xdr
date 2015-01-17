:: from xdr.backends.python.utils import pack_expr

:: if m.kind == "basic":
${pack_expr(m, src)}
:: elif m.kind == "optional":
if ${src} is not None:
    packer.pack_bool(True)
    ${pack_expr(m, src)}
else:
    packer.pack_bool(False)
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
packer.pack_fopaque(${m.length}, ${src})
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
:: if m.length is not None:
assert(len(${src}) <= ${m.length})
:: #endif
packer.pack_opaque(${src})
:: elif m.kind == "array":
assert(len(${src}) == ${m.length})
for x in ${src}:
    ${pack_expr(m, 'x')}
:: elif m.kind == "list":
:: if m.length is not None:
assert(len(${src}) <= ${m.length})
:: #endif
packer.pack_int(len(${src}))
for x in ${src}:
    ${pack_expr(m, 'x')}
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
