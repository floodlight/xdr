XDR Compiler
============

Given an XDR specification (*.x), this program generates code for a target
language.

Usage
-----

Assuming a file myxdr.x with this content:

    struct foo {
        int a;
        string b<>;
    };

You can generate Python code like this:

    xdr -t python -o myxdr myxdr.x

Then in a Python program:

    import myxdr
    x = myxdr.foo(a=1, b="bar")
    data = x.pack()
    y = myxdr.foo.unpack(data)
    assert x == y

References
----------

 - [RFC 4506](http://tools.ietf.org/html/rfc4506)
