# -*- coding: utf-8 -*-

import ast

class PowTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if node.op.__class__ != ast.Pow:
            return node
        # math.pow
        dummy_math = ast.Name(id="math", ctx=ast.Load())
        dummy_func = ast.Attribute(value=dummy_math, attr="pow", ctx=ast.Load())
        return ast.Call(func=dummy_func, args=[node.left, node.right], keywords=[], starargs=None, kwargs=None)


class FloorDivTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if node.op.__class__ != ast.FloorDiv:
            return node
        dummy_op = ast.BinOp(left=node.left, op=ast.Div(), right=node.right)
        dummy_int = ast.Name(id="int", ctx=ast.Load())
        return ast.Call(func=dummy_int, args=[dummy_op], keywords=[], starargs=None, kwargs=None)


Transformers = [
    PowTransformer,
    FloorDivTransformer,
]
