# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ast

import six

from . import cpp
from . import docstring


class Hook(object):
    def __init__(self, visitor):
        self.visitor = visitor

    def match(self, node):
        raise NotImplementedError

    def apply(self, node, ret):
        raise NotImplementedError


class ExprHook(Hook):
    pass


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


class NoneHook(CallHook):
    def match(self, node):
        if six.PY3:
            if node.__class__ != ast.NameConstant:
                return False
            return node.value is None
        elif six.PY2:
            if node.__class__ != ast.Name:
                return False
            return node.id == "None"

    def apply(self, node, ret):
        ret = cpp.Name(id="nullptr")
        return ret


class ArgTypeHook(CallHook):
    def match(self, node):
        return node.__class__ == ast.FunctionDef

    def apply(self, node, ret):
        if ret.docstring is None:
            return ret
        for type in docstring.get_params(ret.docstring):
            ret.args.set_arg_type(type["param"], cpp.type_registry.convert(type["type"]))
        return ret


class RangeHook(CallHook):
    def match(self, node):
        if node.__class__ != ast.Call:
            return False
        func = node.func
        if func.__class__ != ast.Name:
            return False
        return func.id == "range"

    def apply(self, node, ret):
        ret.func = cpp.CppScope(value=cpp.Name(id="py2cpp"), attr="range")
        return ret


class PrintHook(ExprHook):
    def match(self, node):
        if node.__class__ != ast.Expr:
            return False
        value = node.value
        if value.__class__ != ast.Call:
            return False
        if value.func.__class__ != ast.Name:
            return False
        return value.func.id == "print"

    def apply(self, node, ret):
        ret = cpp.StdCout(value=ret.value)
        return ret


Hooks = [
    MathPowHook,
    TupleHook,
    NoneHook,
    ArgTypeHook,
    RangeHook,
    PrintHook,
]
