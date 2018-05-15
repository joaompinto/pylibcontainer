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

name = "pylibcontainer"

setup(
    version=open(join(name, 'version')).readline().strip("\r\n"),
    install_requires=[x for x in requirements.splitlines() if x],
    packages = find_packages(),
    entry_points='''
        [console_scripts]
        pylibcontainer=pylibcontainer.__main__:pylibcontainer
        '''
)
