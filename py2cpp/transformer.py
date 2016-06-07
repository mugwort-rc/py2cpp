# -*- coding: utf-8 -*-

import ast


class PrintTransformer(ast.NodeTransformer):
    """for Python2"""
    def visit_Print(self, node):
        if node.__class__ != ast.Print:
            return node
        dummy_func = ast.Name(id="print", ctx=ast.Load())
        keywords = []
        if not node.nl:
            end = ast.keyword(arg="end", value=ast.Str(s=""))
            keywords.append(end)
        dummy_call = ast.Call(func=dummy_func, args=node.values, keywords=keywords, starargs=None, kwargs=None)
        return ast.Expr(value=dummy_call)


class TupleTransformer(ast.NodeTransformer):
    def visit_Tuple(self, node):
        if node.__class__ != ast.Tuple:
            return node
        dummy_func = ast.Name(id="tuple", ctx=ast.Load())
        return ast.Call(func=dummy_func, args=node.elts, keywords=[], starargs=None, kwargs=None)


class PowTransformer(ast.NodeTransformer):
    def visit_AugAssign(self, node):
        if node.op.__class__ != ast.Pow:
            return node
        dummy_math = ast.Name(id="math", ctx=ast.Load())
        dummy_func = ast.Attribute(value=dummy_math, attr="pow", ctx=ast.Load())
        dummy_call = ast.Call(func=dummy_func, args=[node.target, node.value], keywords=[], starargs=None, kwargs=None)
        return ast.Assign(targets=[node.target], value=dummy_call)

    def visit_BinOp(self, node):
        if node.op.__class__ != ast.Pow:
            return node
        # math.pow
        dummy_math = ast.Name(id="math", ctx=ast.Load())
        dummy_func = ast.Attribute(value=dummy_math, attr="pow", ctx=ast.Load())
        return ast.Call(func=dummy_func, args=[node.left, node.right], keywords=[], starargs=None, kwargs=None)


class FloorDivTransformer(ast.NodeTransformer):
    def visit_AugAssign(self, node):
        if node.op.__class__ != ast.FloorDiv:
            return node
        dummy_op = ast.BinOp(left=node.target, op=ast.Div(), right=node.value)
        dummy_int = ast.Name(id="int", ctx=ast.Load())
        dummy_call = ast.Call(func=dummy_int, args=[dummy_op], keywords=[], starargs=None, kwargs=None)
        return ast.Assign(targets=[node.target], value=dummy_call)

    def visit_BinOp(self, node):
        if node.op.__class__ != ast.FloorDiv:
            return node
        dummy_op = ast.BinOp(left=node.left, op=ast.Div(), right=node.right)
        dummy_int = ast.Name(id="int", ctx=ast.Load())
        return ast.Call(func=dummy_int, args=[dummy_op], keywords=[], starargs=None, kwargs=None)


Transformers = [
    PrintTransformer,
    TupleTransformer,
    PowTransformer,
    FloorDivTransformer,
]
