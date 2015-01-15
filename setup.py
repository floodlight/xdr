#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'xdr',
    'description': 'XDR compiler targeting multiple languages',
    'author': 'Rich Lane',
    'url': 'http://github.com/floodlight/xdr',
    'author_email': 'rlane@bigswitch.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['xdr'],
    'scripts': ['bin/xdr']
}

setup(**config)
