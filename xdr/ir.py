"""
Intermediate Representation (IR)

This file is intended to be imported as "from xdr.ir import *".
"""

from collections import namedtuple

XDRStruct = namedtuple("XDRStruct", ["name", "members"])
XDRDeclaration = namedtuple("XDRDeclaration", ["name", "kind", "type", "length"])
XDREnum = namedtuple("XDREnum", ["name", "members"])
XDREnumMember = namedtuple("XDREnumMember", ["name", "value"])
XDRConst = namedtuple("XDRConst", ["name", "value"])
XDRTypedef = namedtuple("XDRTypedef", ["declaration"])
XDRUnion = namedtuple("XDRUnion", ["name", "discriminant", "members"])
XDRUnionMember = namedtuple("XDRUnionMember", ["case", "declaration"])

__all__ = [
    'XDRStruct', 'XDRDeclaration', 'XDREnum', 'XDREnumMember',
    'XDRConst', 'XDRTypedef', 'XDRUnion', 'XDRUnionMember',
]
