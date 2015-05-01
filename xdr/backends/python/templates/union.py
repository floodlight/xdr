:: from xdr.backends.python.utils import literal
class ${union.name}(XDRUnion):
    @classmethod
    def unpack_from(cls, unpacker):
        discriminant = unpacker.unpack_int()
:: for m in union.members:
        if discriminant == ${literal(m.case, constants)}:
            return cls.${m.declaration.name}.unpack_from(unpacker)
:: #endfor
:: for m in union.members:

    class ${m.declaration.name}(XDRUnionMember):
        @classmethod
        def pack_into(cls, packer, obj):
            packer.pack_int(${literal(m.case, constants)})
:: include_indented("_pack.py", indent=12, m=m.declaration, src="obj.value")

        @classmethod
        def unpack_from(cls, unpacker):
            obj = cls()
:: include_indented("_unpack.py", indent=12, m=m.declaration, dst="obj.value")
            return obj
:: #endfor
