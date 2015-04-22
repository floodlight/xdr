import xdrlib

class XDREnum(object):
    __slots__ = ['name', 'value']

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __cmp__(x, y):
        return cmp(int(x), int(y))

    def __hash__(self):
        return hash(int(self))

    @classmethod
    def unpack_from(cls, reader):
        value = reader.unpack_int()
        return cls.members[value]

    @classmethod
    def pack_into(cls, packer, value):
        packer.pack_int(value)

class XDRStruct(object):
    __slots__ = []

    def pack(self):
        packer = xdrlib.Packer()
        self.pack_into(packer, self)
        return packer.get_buffer()

    @classmethod
    def unpack(cls, data):
        return cls.unpack_from(xdrlib.Unpacker(data))

    def __str__(self):
        return repr(self)

class XDRUnion(object):
    @classmethod
    def unpack(cls, data):
        return cls.unpack_from(xdrlib.Unpacker(data))

    @classmethod
    def pack_into(cls, packer, obj):
        type(obj).pack_into(packer, obj)

class XDRUnionMember(object):
    __slots__ = ["value"]

    def __init__(self, value=None):
        self.value = value

    def pack(self):
        packer = xdrlib.Packer()
        self.pack_into(packer, self)
        return packer.get_buffer()

    def __repr__(self):
        return type(self).__name__ + '(' + repr(self.value) + ')'

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __ne__(self, other):
        return not self == other
