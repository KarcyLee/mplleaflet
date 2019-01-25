#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
from setuptools import setup,find_packages


# Dependencies.
with open('requirements.txt') as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]

with open('AUTHORS.md') as f:
    authors = f.read()

description = "Convert Matplotlib plots into Leaflet web maps"
long_description = description + "\n\n" + authors
NAME = "mplleaflet"
AUTHOR = "Jacob Wasserman"
AUTHOR_EMAIL = "jwasserman@gmail.com"
MAINTAINER = "Jacob Wasserman"
MAINTAINER_EMAIL = "jwasserman@gmail.com"
DOWNLOAD_URL = 'http://github.com/jwass/mplleaflet'
LICENSE = 'BSD 3-clause'
VERSION = '0.0.5'

setup(
    name=NAME,
    version=VERSION,
    description=description,
    long_description=long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    packages=["mplleaflet", "mplleaflet.templates", "mplleaflet.mplexporter", "mplleaflet.mplexporter.renderers"],
    # Include the templates
    package_data={'': ['*.html']},
    tests_require=['pytest'],
    install_requires=install_requires,
    zip_safe=False,
)