# -*- coding: utf-8 -*-

# Copyright 2015 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages
from htmlmin import __version__

README = open('README.rst').read()

setup(
    name='django-htmlmin',
    version=__version__,
    description='html minify for django',
    long_description=README,
    author='CobraTeam',
    author_email='andrewsmedina@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['argparse', 'beautifulsoup4', 'html5lib'],
    tests_require=['django'],
    entry_points={
        'console_scripts': [
            'pyminify = htmlmin.commands:main',
        ],
    },
)
