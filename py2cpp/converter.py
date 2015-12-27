# -*- coding: utf-8 -*-

import ast

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

    def visit_Expr(self, node):
        return cpp.Expr(self.visit(node.value))

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
