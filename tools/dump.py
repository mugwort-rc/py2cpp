#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys
import os

import ast


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))

    args = parser.parse_args(argv)

    node = ast.parse(args.input.read())
    print(ast.dump(node))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
