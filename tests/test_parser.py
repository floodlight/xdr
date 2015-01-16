#!/usr/bin/env python
import unittest
from xdr.parser import parse_ast, parse
from xdr.ir import *

unittest.TestCase.maxDiff = None

class StructTests(unittest.TestCase):
    def test_parse(self):
        src = """\
struct foo {
    int a;
    unsigned int b;
    hyper c;
    unsigned hyper d;
    float e;
    double f;
    quadruple f2;
    bool g;
    void;
    int *i;
    int j[2];
    int k[X];
    int l<2>;
    int m<>;
    opaque n[2];
    opaque o<2>;
    opaque p<>;
    string q<2>;
    string r<>;
    foo s;
};
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['struct',
                'foo',
                [[['int'], 'a'],
                [['unsigned', 'int'], 'b'],
                [['hyper'], 'c'],
                [['unsigned', 'hyper'], 'd'],
                [['float'], 'e'],
                [['double'], 'f'],
                [['quadruple'], 'f2'],
                [['bool'], 'g'],
                ['void'],
                [['int'], '*', 'i'],
                [['int'], 'j', '[', 2, ']'],
                [['int'], 'k', '[', 'X', ']'],
                [['int'], 'l', '<', 2, '>'],
                [['int'], 'm', '<', '>'],
                ['opaque', 'n', '[', 2, ']'],
                ['opaque', 'o', '<', 2, '>'],
                ['opaque', 'p', '<', '>'],
                ['string', 'q', '<', 2, '>'],
                ['string', 'r', '<', '>'],
                [['foo'], 's']]]])

        ir = parse(src)
        self.assertEquals(ir, [
            XDRStruct(name='foo', members=[
                XDRDeclaration(name='a', kind='basic', type='int', length=None),
                XDRDeclaration(name='b', kind='basic', type='unsigned int', length=None),
                XDRDeclaration(name='c', kind='basic', type='hyper', length=None),
                XDRDeclaration(name='d', kind='basic', type='unsigned hyper', length=None),
                XDRDeclaration(name='e', kind='basic', type='float', length=None),
                XDRDeclaration(name='f', kind='basic', type='double', length=None),
                XDRDeclaration(name='f2', kind='basic', type='quadruple', length=None),
                XDRDeclaration(name='g', kind='basic', type='bool', length=None),
                XDRDeclaration(name=None, kind='basic', type='void', length=None),
                XDRDeclaration(name='i', kind='optional', type='int', length=None),
                XDRDeclaration(name='j', kind='array', type='int', length=2),
                XDRDeclaration(name='k', kind='array', type='int', length='X'),
                XDRDeclaration(name='l', kind='list', type='int', length=2),
                XDRDeclaration(name='m', kind='list', type='int', length=None),
                XDRDeclaration(name='n', kind='array', type='opaque', length=2),
                XDRDeclaration(name='o', kind='list', type='opaque', length=2),
                XDRDeclaration(name='p', kind='list', type='opaque', length=None),
                XDRDeclaration(name='q', kind='list', type='string', length=2),
                XDRDeclaration(name='r', kind='list', type='string', length=None),
                XDRDeclaration(name='s', kind='basic', type='foo', length=None),
            ])
        ])

class EnumTests(unittest.TestCase):
    def test_ast(self):
        src = """\
enum foo {
    a = 1,
    b = 2
};
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['enum', 'foo', [['a', 1], ['b', 2]]]])

        ir = parse(src)
        self.assertEquals(ir, [
            XDREnum(name='foo', members=[
                XDREnumMember(name='a', value=1),
                XDREnumMember(name='b', value=2),
            ])
        ])

class TypedefTests(unittest.TestCase):
    def test_ast(self):
        src = """\
typedef opaque foo<3>;
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['typedef', ['opaque', 'foo', '<', 3, '>']]])

        ir = parse(src)
        self.assertEquals(ir, [
            XDRTypedef(XDRDeclaration(name='foo', kind='list', type='opaque', length=3)),
        ])

class UnionTests(unittest.TestCase):
    def test_ast(self):
        src = """\
union foo switch(int type) {
    case 1: int a;
    case 2:
    case 3:
        float b;
    default:
        opaque c<>;
};
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['union',
                'foo',
                [['int'], 'type'],
                [
                    [[1], [['int'], 'a']],
                    [[2, 3], [['float'], 'b']],
                    ['default', ['opaque', 'c', '<', '>']],
                ]]])

        ir = parse(src)
        self.assertEquals(ir, [
            XDRUnion(name='foo',
                discriminant=XDRDeclaration(name='type', kind='basic', type='int', length=None),
                members=[
                    XDRUnionMember(cases=[1], declaration=XDRDeclaration(name='a', kind='basic', type='int', length=None)),
                    XDRUnionMember(cases=[2, 3], declaration=XDRDeclaration(name='b', kind='basic', type='float', length=None)),
                    XDRUnionMember(cases='default', declaration=XDRDeclaration(name='c', kind='list', type='opaque', length=None)),
                ])])

class ConstantTests(unittest.TestCase):
    def test_ast(self):
        src = """\
const a = 0;
const b = 42;
const c = -42;
const d = 0777;
const e = 0xffffffff;
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['const', 'a', 0],
             ['const', 'b', 42],
             ['const', 'c', -42],
             ['const', 'd', 0777],
             ['const', 'e', 0xffffffff]])

        ir = parse(src)
        self.assertEquals(ir, [
            XDRConst(name='a', value=0),
            XDRConst(name='b', value=42),
            XDRConst(name='c', value=-42),
            XDRConst(name='d', value=511),
            XDRConst(name='e', value=4294967295),
        ])

if __name__ == '__main__':
    unittest.main()
