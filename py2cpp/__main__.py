#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys
import os

import ast

from py2cpp.converter import Converter
from py2cpp.cpp import BuildContext


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))
    parser.add_argument("--using-qt", action="store_true")

    args = parser.parse_args(argv)

    if args.using_qt:
        from py2cpp import qt

    node = ast.parse(args.input.read())
    conv = Converter()
    cpp_node = conv.visit(node)

    ctx = BuildContext.create()
    print("// generate by py2cpp")
    print("// original source code:", args.input.name)
    print('#include "py2cpp/py2cpp.hpp"\n')
    print(cpp_node.build(ctx))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
