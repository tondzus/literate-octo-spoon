#!/usr/bin/env python3
from distutils.core import setup
from setuptools import find_packages


setup(
    name='pycoins',
    version='0.1',
    description='Bitcoin history analyzer',
    author='Tomas Stibrany',
    author_email='tms.stibrany@gmail.com',
    url='https://github.com/tondzus/pycoins',
    packages=find_packages(),
    requires=['requests', 'sqlalchemy', 'pandas'],
)
