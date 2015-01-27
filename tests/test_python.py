#!/usr/bin/env python
import unittest
import xdr
import tempfile
import os
import imp
import xdrlib
import subprocess
import shutil
import sys

root = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def pack(*xs):
    """
    Low-level XDR encoder for tests

    Only supports ints and fixed length strings. You can construct
    any XDR message from these primitives. It's a cleaner syntax
    for binary data.
    """
    packer = xdrlib.Packer()
    for x in xs:
        if isinstance(x, int):
            packer.pack_int(x)
        elif isinstance(x, str):
            packer.pack_fopaque(len(x), x)
        else:
            assert(False)
    return packer.get_buffer()

class XDRTestCase(unittest.TestCase):
    maxDiff = None

    def __init__(self, *args, **kwargs):
        self.tmpdirs = []
        unittest.TestCase.__init__(self, *args, **kwargs)

    def load_xdr(self, name):
        """
        Run bin/xdr on a file from tests/xdr/, then import it

        Returns the imported module
        """
        modulename = os.path.splitext(name)[0] + '_xdr'
        if modulename in sys.modules:
            return sys.modules[modulename]
        bindir = os.path.join(root, "bin")
        filename = os.path.join(root, "tests", "xdr", name)
        tmpdir = tempfile.mkdtemp(prefix="xdr-test-python.")
        outdir = os.path.join(tmpdir, modulename)
        self.tmpdirs.append(tmpdir)
        subprocess.check_call([bindir+"/xdr", "-t", "python", "-o", outdir, filename])
        return imp.load_source(modulename, outdir + '/__init__.py')

    def tearDown(self):
        # Delete temporary directories if the test passed
        if sys.exc_info() == (None, None, None):
            for tmpdir in self.tmpdirs:
                shutil.rmtree(tmpdir)

class PackTests(XDRTestCase):
    def test_struct(self):
        proto = self.load_xdr("struct.x")
        x = proto.foo(a=1, b=[2, proto.X, proto.bar.J],
                      c=[5], d="bar", e="\x00\x01", f=proto.bar.I)
        expected = pack(1, 2, 3, 200, 1, 5, 3, "bar", 2, "\x00\x01", 100)
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

    def test_union(self):
        proto = self.load_xdr("union.x")

        x = proto.foo.a(42)
        expected = pack(1, 42)
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

        x = proto.foo.b(64)
        expected = pack(2, 64)
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

        x = proto.foo.c("ABC")
        expected = pack(3, 3, "ABC")
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

        x = proto.foo.d(proto.bar(a=1, b=2))
        expected = pack(4, 1, 2)
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

    def test_typedef(self):
        proto = self.load_xdr("typedef.x")

        x = proto.foo(a=1, b=False, c="ABC", d="DE")
        expected = pack(1, 0, 3, "ABC", "DE")
        self.assertEquals(x.pack(), expected)
        y = proto.foo.unpack(expected)
        self.assertEquals(x, y)
        self.assertEquals(y.pack(), expected)

class StringTests(XDRTestCase):
    def test_enum_string(self):
        proto = self.load_xdr("struct.x")
        self.assertEquals(repr(proto.bar.I), "bar.I")
        self.assertEquals(str(proto.bar.I), "bar.I")

    def test_struct_string(self):
        proto = self.load_xdr("struct.x")
        x = proto.foo(a=1, b=[2, proto.X, 4],
                      c=[5], d="bar", e="\x00\x01", f=proto.bar.I)
        expected = "foo(a=1, b=[2, 3, 4], c=[5], d='bar', e='\\x00\\x01', f=bar.I)"
        self.assertEquals(repr(x), expected)
        self.assertEquals(str(x), expected)
