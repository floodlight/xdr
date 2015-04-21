:: # Given an XDRDeclaration 'm' and a destination variable 'dst', this template
:: # generates deserialization code.
:: from xdr.backends.lua.pack import unpacker, literal
:: if m.kind == "basic":
:: # Plain
:: # int x
${dst} = ${unpacker(m.type)}(reader)
::
:: elif m.kind == "optional":
:: # Optional
:: # int *x
${dst} = read_optional(reader, ${unpacker(m.type)})
::
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
:: # Fixed length string
:: # string x[2]
${dst} = read_fstring(reader, ${literal(m.length, constants)})
::
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
:: # Variable length string
:: # string x<2>
${dst} = read_string(reader, ${literal(m.length, constants)})
::
:: elif m.kind == "array":
:: # Fixed length array
:: # int x[2]
${dst} = read_array(reader, ${unpacker(m.type)}, ${literal(m.length, constants)})
::
:: elif m.kind == "list":
:: # Variable length array
:: # int x<2>
${dst} = read_list(reader, ${unpacker(m.type)}, ${literal(m.length, constants)})
::
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
