# -*- coding: utf-8 -*-
"""
Copyright 2016 django-htmlmin authors. All rights reserved.
Use of this source code is governed by a BSD-style
license that can be found in the LICENSE file.
"""
import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, '__init__.py')) as fp:
        init_py = fp.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('htmlmin')

with open('README.rst', 'r') as fp:
    README = fp.read()

setup(
    name='django-htmlmin',
    version=version,
    description='HTML minifier for Python frameworks (not only Django, '
                'despite the name).',
    long_description=README,
    author='CobraTeam',
    author_email='andrewsmedina@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['beautifulsoup4', 'html5lib'],
    tests_require=['django'],
    entry_points={
        'console_scripts': [
            'pyminify = htmlmin.commands:main',
        ],
    },
    keywords='django, html, minifier, minify',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
