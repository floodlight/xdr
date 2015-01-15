#!/usr/bin/env python
import unittest
from xdr.parser import parse_ast

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

class TypedefTests(unittest.TestCase):
    def test_ast(self):
        src = """\
typedef opaque foo<3>;
"""
        ast = parse_ast(src)
        self.assertEquals(ast,
            [['typedef', ['opaque', 'foo', '<', 3, '>']]])

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

if __name__ == '__main__':
    unittest.main()
