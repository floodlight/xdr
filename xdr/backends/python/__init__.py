"""
Python backend

Creates one __init__.py file in the output directory. Classes are generated for
structs, enums, and unions. Each class has pack and unpack methods to convert
the Python objects to and from XDR encoded strings.

Usage:

    import myxdr
    x = myxdr.foo(a=1, b="bar")
    data = x.pack()
    y = myxdr.foo.unpack(data)
    assert x == y
"""
import os
from xdr.parser import *
from template_utils import render_template

def generate(ir, output):
    os.mkdir(output)
    out = open(os.path.join(output, "__init__.py"), 'w')

    render_template(out, "header.py", {})

    for x in ir:
        out.write("\n")
        if isinstance(x, XDRConst):
            render_template(out, "const.py", dict(const=x))
        elif isinstance(x, XDREnum):
            render_template(out, "enum.py", dict(enum=x))
        elif isinstance(x, XDRStruct):
            render_template(out, "struct.py", dict(struct=x))
        elif isinstance(x, XDRUnion):
            render_template(out, "union.py", dict(union=x))
        elif isinstance(x, XDRTypedef):
            render_template(out, "typedef.py", dict(typedef=x))

    out.write("\n__all__ = " + repr([x.name for x in ir if not isinstance(x, XDRTypedef)]))
