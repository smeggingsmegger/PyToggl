#!/usr/bin/env python
#coding:utf-8
# Author:  smeggingsmegger
# Purpose: setup
# Created: 2014-10-02
#
# The MIT License (MIT)

# Copyright (c) 2013 Scott Blevins

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

long_description = read('README.md')

if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='PyToggl',
    version='0.2.1',
    url='http://github.com/smeggingsmegger/PyToggl',
    license='MIT',
    author='Scott Blevins',
    author_email='sblevins@gmail.com',
    description='The Definitive Python Library For The Toggl API',
    long_description= long_description+'\n'+read('CHANGES'),
    platforms='OS Independent',
    packages=['PyToggl'],
    include_package_data=True,
    install_requires=['requests'],
    keywords=['Toggl', 'Time', 'Tracking', 'Library', 'API'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
