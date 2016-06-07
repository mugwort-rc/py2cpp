# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ast

from . import cpp

class Hook(object):
    def __init__(self, visitor):
        self.visitor = visitor

    def match(self, node):
        raise NotImplementedError

    def apply(self, node, ret):
        raise NotImplementedError


class CallHook(Hook):
    pass


class MathPowHook(CallHook):
    def match(self, node):
        if node.__class__ != ast.Call:
            return False
        func = node.func
        if node.func.__class__ != ast.Attribute:
            return False
        if node.func.value.__class__ != ast.Name:
            return False
        return node.func.value.id == "math" and node.func.attr == "pow"

    def apply(self, node, ret):
        ret.func = cpp.CppScope(value=cpp.Name(id="std"), attr="pow")
        return ret


class TupleHook(CallHook):
    def match(self, node):
        if node.__class__ != ast.Call:
            return False
        func = node.func
        if node.func.__class__ != ast.Name:
            return False
        return node.func.id == "tuple"

    def apply(self, node, ret):
        ret.func = cpp.CppScope(value=cpp.Name(id="std"), attr="make_tuple")
        return ret


Hooks = [
    MathPowHook,
    TupleHook,
]
