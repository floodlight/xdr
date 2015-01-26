"""
Python backend

TODO
 - Typedefs
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
