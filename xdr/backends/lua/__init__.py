"""
Lua backend

This backend converts XDR encoded data to and from plain Lua tables.
It requires the user to provide "reader" and "writer" objects that handle
the low level serialization. See MockReader and MockWriter in the tests
directory for examples. This is done to allow the user to implement the
reader/writer in the most performant way possible, for example by using
the LuaJIT FFI.

Usage:

    local myxdr = require("myxdr/xdr")
    local foo = myxdr.read_foo(reader)
    foo.a = foo.a + 1
    myxdr.write_foo(writer, foo)
"""
import os
import tenjin
from xdr.parser import *

def collect_constants(ir):
    constants = {}
    for x in ir:
        if isinstance(x, XDRConst):
            assert x.name not in constants
            constants[x.name] = x.value
        elif isinstance(x, XDREnum):
            for m in x.members:
                assert m.name not in constants
                constants[m.name] = m.value
    return constants

def generate(ir, output):
    os.mkdir(output)
    out = open(os.path.join(output, "xdr.lua"), 'w')

    constants = collect_constants(ir)

    render_template(out, "header.lua", {})

    for x in ir:
        out.write("\n")
        if isinstance(x, XDRConst):
            render_template(out, "const.lua", dict(const=x))
        elif isinstance(x, XDREnum):
            render_template(out, "enum.lua", dict(enum=x))
        elif isinstance(x, XDRStruct):
            render_template(out, "struct.lua", dict(struct=x, constants=constants))
        elif isinstance(x, XDRUnion):
            render_template(out, "union.lua", dict(union=x, constants=constants))
        elif isinstance(x, XDRTypedef):
            render_template(out, "typedef.lua", dict(typedef=x, constants=constants))

    render_template(out, "footer.lua", {})

def render_template(out, name, context):
    """
    Render a template using tenjin.
    out: a file-like object
    name: name of the template
    context: dictionary of variables to pass to the template
    """
    path = [os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')]
    pp = [ tenjin.PrefixedLinePreprocessor() ] # support "::" syntax
    template_globals = { "to_str": str, "escape": str } # disable HTML escaping
    engine = tenjin.Engine(path=path, pp=pp)
    out.write(engine.render(name, context, template_globals))
