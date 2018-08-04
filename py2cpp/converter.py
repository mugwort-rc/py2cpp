# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ast

import six

from . import cpp
from . import hook
from . import transformer

BOOLOP_MAP = {
    ast.And: "&&",
    ast.Or: "||",
}

OPERATOR_MAP = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Mod: "%",
    #ast.Pow: "**",  # special case
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    #ast.FloorDiv: "//",  # special case
}

UNARYOP_MAP = {
    ast.Invert: "~",
    ast.Not: "!",
    ast.UAdd: "+",
    ast.USub: "-",
}

CMPOP_MAP = {
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    #ast.Is: " is ",  # special case
    #ast.IsNot: " is not ",  # special case
    #ast.In: " in ",  # special case
    #ast.NotIn: " not in ",  # special case
}

class Converter(ast.NodeVisitor):
    def __init__(self, transformers=transformer.Transformers, hooks=hook.Hooks):
        """
        :type transformers: list of NodeTransformer
        """
        self.transformers = [x() for x in transformers]
        self.hooks = [x(self) for x in hooks]
        self.arguments = []

    def visit(self, node):
        ret = super(Converter, self).visit(node)
        if ret is None:
            return cpp.UnsupportedNode(node)
        for hook in self.hooks:
            if hook.match(node):
                return hook.apply(node, ret)
        return ret

    #
    # Module
    #

    def visit_Module(self, node):
        # apply transformers
        for transformer in self.transformers:
            node = transformer.visit(node)
        return cpp.Module(body=[self.visit(x) for x in node.body])

    #
    # Statements
    #

    def visit_FunctionDef(self, node):
        name = node.name
        args = self.visit(node.args)
        body = [self.visit(x) for x in node.body]
        docstring = ast.get_docstring(node)
        if docstring:
            body = body[1:]
        if hasattr(node, "returns"):
            returns = self.visit(node.returns)
        else:
            returns = None
        # TODO: decorator_list
        return cpp.FunctionDef(name=name, args=args, body=body, docstring=docstring, returns=returns)

    def visit_ClassDef(self, node):
        name = node.name
        bases = [self.visit(x) for x in node.bases]
        if six.PY3:
            keywords = [self.visit(x) for x in node.keywords]
        body = [self.visit(x) for x in node.body]
        docstring = ast.get_docstring(node)
        if docstring:
            body = body[1:]
        # TODO: decorator_list
        if six.PY3:
            return cpp.ClassDef(name=name, bases=bases, keywords=keywords, body=body, docstring=docstring)
        else:
            return cpp.ClassDef(name=name, bases=bases, body=body, docstring=docstring)

    def visit_Return(self, node):
        if node.value:
            value = self.visit(node.value)
        else:
            value = None
        return cpp.Return(value=value)

    def visit_Assign(self, node):
        targets = [self.visit(x) for x in node.targets]
        value = self.visit(node.value)
        return cpp.Assign(targets, value)

    def visit_AugAssign(self, node):
        assert node.op.__class__ not in [ast.Pow, ast.FloorDiv]
        target = self.visit(node.target)
        op = OPERATOR_MAP[node.op.__class__]
        value = self.visit(node.value)
        return cpp.AugAssign(target, op, value)

    def visit_For(self, node):
        target = self.visit(node.target)
        iter = self.visit(node.iter)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return cpp.For(target=target, iter=iter, body=body, orelse=orelse)

    def visit_While(self, node):
        test = self.visit(node.test)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return cpp.While(test=test, body=body, orelse=orelse)

    def visit_If(self, node):
        test = self.visit(node.test)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return cpp.If(test=test, body=body, orelse=orelse)

    def visit_Raise(self, node):
        if six.PY3:
            exc = self.visit(node.exc) if node.exc else None
            cause = self.visit(node.cause) if node.cause else None
            return cpp.Raise(exc=exc, cause=cause)
        elif six.PY2:
            type = self.visit(node.type) if node.type else None
            inst = self.visit(node.inst) if node.inst else None
            tback = self.visit(node.tback) if node.tback else None
            return cpp.Raise(type=type, inst=inst, tback=tback)

    def visit_Expr(self, node):
        return cpp.Expr(self.visit(node.value))

    def visit_Pass(self, node):
        return cpp.Pass()

    def visit_Break(self, node):
        return cpp.Break()

    def visit_Continue(self, node):
        return cpp.Continue()

    #
    # Expressions
    #

    def visit_BoolOp(self, node):
        op = BOOLOP_MAP[node.op.__class__]
        return cpp.BoolOp(op=op, values=[self.visit(x) for x in node.values])

    def visit_BinOp(self, node):
        assert node.op.__class__ not in [ast.Pow, ast.FloorDiv]
        left = self.visit(node.left)
        op = OPERATOR_MAP[node.op.__class__]
        right = self.visit(node.right)
        return cpp.BinOp(left=left, op=op, right=right)

    def visit_UnaryOp(self, node):
        op = UNARYOP_MAP[node.op.__class__]
        operand = self.visit(node.operand)
        return cpp.UnaryOp(op=op, operand=operand)

    def visit_Lambda(self, node):
        args = self.visit(node.args)
        body = self.visit(node.body)
        return cpp.Lambda(args=args, body=body)

    def visit_IfExp(self, node):
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return cpp.IfExp(test=test, body=body, orelse=orelse)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        ops = [CMPOP_MAP[x.__class__] for x in node.ops]
        comparators = [self.visit(x) for x in node.comparators]
        return cpp.Compare(left=left, ops=ops, comparators=comparators)

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(x) for x in node.args]
        keywords = [self.visit(x) for x in node.keywords]
        if six.PY2:
            starargs = self.visit(node.starargs) if node.starargs else None
            kwargs = self.visit(node.kwargs) if node.kwargs else None
            return cpp.Call(func, args, keywords, starargs, kwargs)
        return cpp.Call(func, args, keywords)

    def visit_Num(self, node):
        return cpp.Num(node.n)

    def visit_Str(self, node):
        return cpp.Str(s=node.s)

    def visit_NameConstant(self, node):
        """for python3 ast
        """
        value = node.value
        return cpp.NameConstant(value=value)

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        return cpp.Attribute(value, node.attr)

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        slice = self.visit(node.slice)
        return cpp.Subscript(value=value, slice=slice)

    def visit_Name(self, node):
        return cpp.Name(node.id)
        # TODO: node.ctx

    def visit_Tuple(self, node):
        elts = [self.visit(x) for x in node.elts]
        return cpp.Tuple(elts=elts)

    # slice

    def visit_Index(self, node):
        value = self.visit(node.value)
        return cpp.Index(value=value)

    def visit_arguments(self, node):
        args = [self.visit(x) for x in node.args]
        vararg = node.vararg
        kwarg = node.kwarg
        defaults = [self.visit(x) for x in node.defaults]
        ret = cpp.arguments(args=args, vararg=vararg, kwarg=kwarg, defaults=defaults)
        self.arguments.append(ret)
        return ret

    def visit_arg(self, node):
        """for python3 ast
        """
        arg = node.arg
        if hasattr(node, "annotation"):
            annotation = self.visit(node.annotation)
        else:
            annotation = None
        # TODO: node.lineno
        # TODO: node.col_offset
        return cpp.arg(arg=arg, annotation=annotation)

    def visit_keyword(self, node):
        if six.PY3:
            name = node.arg
        else:
            name = node.name
        value = self.visit(node.value)
        return cpp.keyword(name=name, value=value)
