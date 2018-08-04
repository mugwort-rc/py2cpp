#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="py2cpp",
    version="0.0.1",
    description="A Python to C++ compiler",
    url="https://github.com/mugwort-rc/py2cpp",
    license="GPL3",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Compilers"
    ],
    keywords=["python3", "C++", "ast"],
    author="mugwort_rc",
    author_email="mugwort [dot] rc [at] gmail [dot] com",
    zip_safe=False,
    packages=find_packages(),
)
