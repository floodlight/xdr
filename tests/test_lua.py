import tempfile
import os
import subprocess
import shutil
import string
import test_data
from nose.plugins.skip import Skip, SkipTest

root = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
testutils_lua = file(os.path.join(root, "tests", "testutils.lua")).read()

def check_datafile(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    data = test_data.read(filename)
    if not 'lua' in data:
        raise SkipTest("no lua section in datafile")

    tmpdir = tempfile.mkdtemp(prefix="xdr-test-lua.")

    bindir = os.path.join(root, "bin")
    outdir = os.path.join(tmpdir, "xdr")
    filename = os.path.join(tmpdir, "test.xdr")
    with open(filename, 'w') as f: f.write(data['xdr'])
    subprocess.check_call([bindir+"/xdr", "-t", "lua", "-o", outdir, filename])

    with open(os.path.join(tmpdir, "expected.lua"), 'w') as f:
        f.write("return " + data['lua'])

    # Convert the Python list to Lua syntax
    with open(os.path.join(tmpdir, "raw.lua"), 'w') as f:
        f.write('return { ')
        for x in data['raw']:
            if isinstance(x, int):
                f.write(repr(x) + ', ')
            elif isinstance(x, str):
                def lua_escape(c):
                    if c in string.printable and c != '"':
                        return c
                    else:
                        return "\%03d" % ord(c)
                f.write('"' + ''.join(lua_escape(c) for c in x) + '", ')
            else:
                assert(False)
        f.write('}')

    with open(os.path.join(tmpdir, "testutils.lua"), 'w') as f:
        f.write(testutils_lua)

    try:
        subprocess.check_output(["lua", "-l", "testutils", "-e", "runtest()"], cwd=tmpdir, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        print e.output
        print "Temporary directory:", tmpdir
        raise AssertionError("Test failed")

    shutil.rmtree(tmpdir)

def test_datafiles():
    for filename in test_data.list_files():
        yield check_datafile, filename
