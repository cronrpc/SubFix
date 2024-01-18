#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import pkg_resources
from shutil import rmtree
from setuptools import find_packages, setup, Command

NAME = 'SubFix'
DESCRIPTION = 'A tool to read dataset and crate dataset to train TTS.'
URL = 'https://github.com/cronrpc/SubFix'
EMAIL = 'cronrpc'
AUTHOR = 'cronrpc'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0.1.1'

REQUIRED = [
]

EXTRAS = {
}

here = os.path.abspath(os.path.dirname(__file__))
long_description = DESCRIPTION


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['subfix'],
    install_requires=REQUIRED
    + [
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points={
        "console_scripts": ["subfix=subfix.cli:cli"],
    },
    extras_require=EXTRAS,
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
