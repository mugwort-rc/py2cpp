# -*- coding: utf-8 -*-

import ast

import six

import cpp
import hook
import transformer

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
        return [self.visit(x) for x in node.body]

    #
    # Statements
    #

    def visit_FunctionDef(self, node):
        name = node.name
        args = self.visit(node.args)
        body = [self.visit(x) for x in node.body]
        # TODO: decorator_list
        # TODO: returns (python3)
        return cpp.FunctionDef(name=name, args=args, body=body)

    def visit_ClassDef(self, node):
        name = node.name
        bases = [self.visit(x) for x in node.bases]
        if six.PY3:
            keywords = [self.visit(x) for x in node.keywords]
        body = [self.visit(x) for x in node.body]
        # TODO: decorator_list
        if six.PY3:
            return cpp.ClassDef(name=name, bases=bases, keywords=keywords, body=body)
        else:
            return cpp.ClassDef(name=name, bases=bases, body=body)

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

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(x) for x in node.args]
        keywords = [self.visit(x) for x in node.keywords]
        starargs = self.visit(node.starargs) if node.starargs else None
        kwargs = self.visit(node.kwargs) if node.kwargs else None
        return cpp.Call(func, args, keywords, starargs, kwargs)

    def visit_Num(self, node):
        return cpp.Num(node.n)

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        return cpp.Attribute(value, node.attr)

    def visit_Name(self, node):
        return cpp.Name(node.id)
        # TODO: node.ctx

    def visit_arguments(self, node):
        args = [self.visit(x) for x in node.args]
        vararg = node.vararg
        kwarg = node.kwarg
        defaults = [self.visit(x) for x in node.defaults]
        ret = cpp.arguments(args=args, vararg=vararg, kwarg=kwarg, defaults=defaults)
        self.arguments.append(ret)
        return ret

    def visit_keyword(self, node):
        name = node.name
        value = self.visit(node.value)
        return cpp.keyword(name=name, value=value)
