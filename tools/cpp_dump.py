#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os

import ast

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from py2cpp.converter import Converter
from py2cpp import cpp


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))

    args = parser.parse_args(argv)

    node = ast.parse(args.input.read())
    conv = Converter()
    cpp_node = conv.visit(node)

    print(cpp.dump(cpp_node))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
