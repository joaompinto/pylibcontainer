#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install using distutils

Run:
    python setup.py install

to install this package.
"""
from setuptools import setup, find_packages
from os.path import join

with  open('requirements.txt') as r_file:
    requirements = r_file.read()

with  open('README.rst') as r_file:
    long_desc = r_file.read()

name = "pylibcontainer"

setup(
    version=open(join(name, 'version')).readline().strip("\r\n"),
    long_description=long_desc,
    install_requires=[x for x in requirements.splitlines() if x],
    packages=['pylibcontainer'],
    package_data={'pylibcontainer': ['trusted/keyring.gpg']},
    include_package_data=True,
    entry_points='''
        [console_scripts]
        pylibcontainer=pylibcontainer.__main__:pylibcontainer
        '''
)
