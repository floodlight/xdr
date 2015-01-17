class ${typedef.declaration.name}(object):
    @classmethod
    def pack_into(self, packer, obj):
:: include_indented("_pack.py", indent=8, m=typedef.declaration, src="obj")

    @classmethod
    def unpack_from(cls, unpacker):
:: include_indented("_unpack.py", indent=8, m=typedef.declaration, dst="obj")
        return obj
