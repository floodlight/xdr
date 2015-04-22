import tempfile
import os
import imp
import subprocess
import shutil
import sys
import test_data
from nose.tools import assert_equal
from nose.plugins.skip import Skip, SkipTest

root = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def load_xdr(data):
    """
    Compile and load generated Python code into the running process
    """
    modulename = 'test_xdr'
    if modulename in sys.modules:
        del sys.modules[modulename]
    tmpdir = tempfile.mkdtemp(prefix="xdr-test-python.")
    print "tmpdir", tmpdir
    filename = os.path.join(tmpdir, "test.xdr")
    with open(filename, 'w') as f: f.write(data)
    outdir = os.path.join(tmpdir, modulename)
    bindir = os.path.join(root, "bin")
    subprocess.check_call([bindir+"/xdr", "-t", "python", "-o", outdir, filename])
    mod = imp.load_source(modulename, outdir + '/__init__.py')
    return mod, tmpdir

def check_datafile(filename):
    """
    Check that the generated Python code can serialize and deserialize correctly
    """
    data = test_data.read(filename)
    if not 'python' in data:
        raise SkipTest("no python section in datafile")

    mod, tmpdir = load_xdr(data['xdr'])
    x = eval(data['python'], { 'xdr': mod })
    assert_equal(x.pack(), data['binary'])
    y = mod.root.unpack(data['binary'])
    assert_equal(x, y)
    assert_equal(y.pack(), data['binary'])

    if 'python string' in data:
        assert_equal(str(x), data['python string'])
        assert_equal(str(y), data['python string'])

    shutil.rmtree(tmpdir)

def test_datafiles():
    # Nose test generator
    # Creates a testcase for each datafile
    for filename in test_data.list_files():
        yield check_datafile, filename
