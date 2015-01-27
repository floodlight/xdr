class ${struct.name}(XDRStruct):
    __slots__ = ${repr([m.name for m in struct.members])}

    def __init__(self, ${', '.join('%s=None' % m.name for m in struct.members)}):
:: for m in struct.members:
        self.${m.name} = ${m.name}
:: #endfor

    @classmethod
    def pack_into(self, packer, obj):
:: for m in struct.members:
:: include_indented("_pack.py", indent=8, m=m, src="obj." + m.name)
:: #endfor

    @classmethod
    def unpack_from(cls, unpacker):
        obj = ${struct.name}()
:: for m in struct.members:
:: include_indented("_unpack.py", indent=8, m=m, dst="obj." + m.name)
:: #endfor
        return obj

    def __eq__(self, other):
        if type(self) != type(other):
            return False
:: for m in struct.members:
        if self.${m.name} != other.${m.name}:
            return False
:: #endfor
        return True

    def __repr__(self):
        parts = []
        parts.append('${struct.name}(')
:: first = True
:: for m in struct.members:
:: if not first:
        parts.append(", ")
:: else:
:: first = False
:: #endif
        parts.append('${m.name}=')
        parts.append(repr(self.${m.name}))
:: #endfor
        parts.append(')')
        return ''.join(parts)
