:: # Given an XDRDeclaration 'm' and a source expression 'src', this template
:: # generates serialization code.
:: from xdr.backends.lua.pack import packer, literal
::
:: if m.kind == "basic":
:: # Plain
:: # int x
${packer(m.type)}(writer, ${src})
::
:: elif m.kind == "optional":
:: # Optional
:: # int *x
write_optional(writer, ${src}, ${packer(m.type)})
::
:: elif m.kind == "array" and (m.type == "opaque" or m.type == "string"):
:: # Fixed length string
:: # string x[2]
write_fstring(writer, ${src}, ${literal(m.length, constants)})
::
:: elif m.kind == "list" and (m.type == "opaque" or m.type == "string"):
:: # Variable length string
:: # string x<2>
write_string(writer, ${src}, ${literal(m.length, constants)})
::
:: elif m.kind == "array":
:: # Fixed length array
:: # int x[2]
write_array(writer, ${src}, ${packer(m.type)}, ${literal(m.length, constants)})
::
:: elif m.kind == "list":
:: # Variable length array
:: # int x<2>
write_list(writer, ${src}, ${packer(m.type)}, ${literal(m.length, constants)})
::
:: else:
raise NotImplementedError(${repr(str(m))})
:: #endif
